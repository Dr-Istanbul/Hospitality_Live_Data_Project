import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_opentable_dallas():
    """Get Dallas restaurants from OpenTable"""
    
    # Try multiple URL patterns
    url_patterns = [
        "https://www.opentable.com/location/dallas-restaurants",
        "https://www.opentable.com/s?covers=2&dateTime=2025-10-01T19%3A00%3A00&metroId=20&term=dallas",
        "https://www.opentable.com/search?term=dallas&latitude=32.86332&longitude=-96.848335"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i, url in enumerate(url_patterns):
        print(f"Trying pattern {i+1}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for any text content that indicates success
                title = soup.find('title')
                if title:
                    print(f"  Page title: {title.text}")
                
                # Count potential restaurant elements
                restaurant_keywords = ['restaurant', 'dining', 'eats', 'reservation']
                elements_with_keywords = []
                
                for keyword in restaurant_keywords:
                    found = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
                    elements_with_keywords.extend(found)
                
                print(f"  Found {len(set(elements_with_keywords))} elements with restaurant keywords")
                
                # Save this successful response
                with open(f'successful_pattern_{i+1}.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"  ✅ Saved successful response")
                return response.text
                
            time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue
    
    print("❌ All URL patterns failed")
    return None

# Run it
print("=== Testing OpenTable Access ===\\n")
content = get_opentable_dallas()

if content:
    print("\\n✅ Successfully retrieved OpenTable content")
    print("Next: Inspect the saved HTML files to identify the correct selectors")
else:
    print("\\n❌ Could not access OpenTable")
