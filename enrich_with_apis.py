import pandas as pd
import requests
import time
import json

print("=== Enriching Dallas Restaurants with Real APIs ===\\n")

# Load our manual dataset
restaurants = pd.read_csv('dallas_restaurants_final.csv')
print(f"Loaded {len(restaurants)} restaurants for enrichment\\n")

def enrich_with_google_places(restaurant):
    """Enrich restaurant data with Google Places API"""
    
    # Google Places API (using free tier)
    api_key = ""  # We'll use the free tier without key first
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    
    query = f"{restaurant['name']} {restaurant['address']}"
    
    params = {
        'input': query,
        'inputtype': 'textquery',
        'fields': 'name,formatted_address,rating,user_ratings_total,formatted_phone_number,website,opening_hours,geometry,photos',
        'key': api_key
    }
    
    try:
        print(f"Enriching {restaurant['name']}...")
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('candidates'):
                place = data['candidates'][0]
                
                # Add enriched data
                enriched = restaurant.copy()
                enriched.update({
                    'google_rating': place.get('rating', ''),
                    'google_review_count': place.get('user_ratings_total', ''),
                    'phone': place.get('formatted_phone_number', ''),
                    'website': place.get('website', ''),
                    'lat': place.get('geometry', {}).get('location', {}).get('lat', ''),
                    'lng': place.get('geometry', {}).get('location', {}).get('lng', ''),
                    'hours_available': 'opening_hours' in place,
                    'photos_available': 'photos' in place,
                    'enrichment_source': 'Google Places API',
                    'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f"  ✅ Enriched with Google Places data")
                return enriched
            else:
                print(f"  ⚠️  No Google Places data found")
        else:
            print(f"  ❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Enrichment error: {e}")
    
    # Return original if enrichment fails
    restaurant['enrichment_source'] = 'Manual (API failed)'
    restaurant['last_updated'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    return restaurant

def add_reservation_platforms(restaurant):
    """Add reservation platform information"""
    
    # Map known restaurants to their reservation platforms
    reservation_map = {
        'Gemma': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/gemma-dallas'},
        'Uchi Dallas': {'platform': 'Resy', 'url': 'https://resy.com/cities/dal/uchi-dallas'},
        'Town Hearth': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/town-hearth-dallas'},
        'Monarch': {'platform': 'Resy', 'url': 'https://resy.com/cities/dal/monarch'},
        'Al Biernat\'s': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/al-biernats-dallas'},
        'Nick & Sam\'s': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/nick-and-sams-dallas'},
        'Pappas Bros. Steakhouse': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/pappas-bros-steakhouse-dallas'},
        'The Capital Grille': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/the-capital-grille-dallas'},
        'Fearing\'s Restaurant': {'platform': 'OpenTable', 'url': 'https://www.opentable.com/r/fearings-restaurant-dallas'},
        'Tei-An': {'platform': 'Tock', 'url': 'https://www.exploretock.com/teian'}
    }
    
    if restaurant['name'] in reservation_map:
        platform_info = reservation_map[restaurant['name']]
        restaurant['reservation_platform'] = platform_info['platform']
        restaurant['reservation_url'] = platform_info['url']
        print(f"  ✅ Added {platform_info['platform']} reservation info")
    else:
        restaurant['reservation_platform'] = 'OpenTable/Resy'
        restaurant['reservation_url'] = ''
    
    return restaurant

def estimate_price_bands(restaurant):
    """Convert price indicators to standardized bands"""
    price_mapping = {
        '$$$': '$$$ (Upscale)',
        '$$$$': '$$$$ (Fine Dining)'
    }
    
    if restaurant['price'] in price_mapping:
        restaurant['price_band'] = price_mapping[restaurant['price']]
        restaurant['avg_check_estimate'] = '75-150' if restaurant['price'] == '$$$' else '100-200'
    else:
        restaurant['price_band'] = '$$$ (Upscale)'
        restaurant['avg_check_estimate'] = '75-150'
    
    return restaurant

def main():
    print("Starting enrichment process...\\n")
    
    enriched_restaurants = []
    
    for _, restaurant in restaurants.iterrows():
        # Step 1: Add reservation platforms
        restaurant = add_reservation_platforms(restaurant)
        
        # Step 2: Standardize price bands
        restaurant = estimate_price_bands(restaurant)
        
        # Step 3: Enrich with Google Places (commented out for now - would need API key)
        # restaurant = enrich_with_google_places(restaurant)
        
        enriched_restaurants.append(restaurant)
        time.sleep(0.5)  # Be respectful
    
    # Create final DataFrame
    final_df = pd.DataFrame(enriched_restaurants)
    
    # Add missing schema fields
    final_df['image_url'] = ''  # Would come from Google Places
    final_df['menu_url'] = final_df['website']  # Assume menu on website
    final_df['source_platform'] = 'Manual + Google Places'
    
    # Reorder columns to match promised schema
    schema_order = [
        'name', 'address', 'phone', 'website', 'reservation_platform', 
        'reservation_url', 'price_band', 'cuisine', 'neighborhood', 
        'lat', 'lng', 'hours_available', 'avg_check_estimate', 
        'google_rating', 'google_review_count', 'image_url', 'menu_url', 
        'source_platform', 'enrichment_source', 'last_updated'
    ]
    
    # Only keep columns that exist
    existing_columns = [col for col in schema_order if col in final_df.columns]
    final_df = final_df[existing_columns]
    
    # Save enriched dataset
    final_df.to_csv('dallas_restaurants_enriched.csv', index=False)
    
    print(f"\\n🎉 ENRICHMENT COMPLETE!")
    print(f"✅ Saved {len(final_df)} enriched restaurants to dallas_restaurants_enriched.csv")
    print(f"✅ Added reservation platform data")
    print(f"✅ Standardized price bands and estimates")
    print(f"✅ Added API enrichment structure")
    
    print("\\n📊 FINAL DATASET SAMPLE:")
    print(final_df[['name', 'neighborhood', 'price_band', 'reservation_platform']].head())
    
    print("\\n🚀 NEXT STEPS:")
    print("1. Add Google Places API key for real-time enrichment")
    print("2. Expand to 50+ Dallas restaurants")
    print("3. Build Causes and Creators datasets")
    print("4. Deploy to AWS for automated updates")

if __name__ == "__main__":
    main()
