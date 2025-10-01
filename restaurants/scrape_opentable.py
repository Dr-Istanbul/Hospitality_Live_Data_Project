# restaurants/scripts/scrape_opentable.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_opentable_dallas():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    base_url = "https://www.opentable.com/location/dallas-restaurants"
    all_restaurants = []
    
    # Start with first 5 pages to validate
    for page in range(1, 6):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"
            
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # TEMPORARY: Manual extraction - you'll update selectors
            restaurants = extract_restaurants_manual(soup)
            all_restaurants.extend(restaurants)
            
            print(f"Page {page}: Found {len(restaurants)} restaurants")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
    
    # Save initial results
    df = pd.DataFrame(all_restaurants)
    df.to_csv('restaurants/data/opentable_sample.csv', index=False)
    print(f"Saved {len(all_restaurants)} restaurants")
    return all_restaurants

def extract_restaurants_manual(soup):
    """Manual extraction - you'll refine this with actual selectors"""
    restaurants = []
    
    # Look for restaurant containers
    cards = soup.find_all('div', class_=lambda x: x and 'restaurant' in x.lower())
    
    for card in cards[:10]:  # Just get first 10 for testing
        try:
            restaurant = {
                'name': 'Gemma',  # Placeholder - you'll extract real data
                'neighborhood': 'Knox/Henderson',
                'cuisine': 'American, Contemporary', 
                'price_band': '$$$',
                'reservation_url': 'https://www.opentable.com/r/gemma-dallas',
                'source_platform': 'OpenTable'
            }
            restaurants.append(restaurant)
        except:
            continue
            
    return restaurants