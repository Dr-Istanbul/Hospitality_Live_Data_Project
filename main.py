# main.py
from restaurants.scripts.scrape_opentable import scrape_opentable_dallas
from causes.scripts.scrape_directories import scrape_school_directories  
from creators.scripts.scrape_hashtags import scrape_instagram_hashtags
import pandas as pd

def main():
    print("Starting Dallas Data Collection...")
    
    # Run all three in sequence
    print("1. Scraping restaurants...")
    restaurants = scrape_opentable_dallas()
    
    print("2. Scraping causes...") 
    causes = scrape_school_directories()
    
    print("3. Scraping creators...")
    creators = scrape_instagram_hashtags()
    
    # Save initial results
    pd.DataFrame(restaurants).to_csv('restaurants/data/initial_sample.csv')
    pd.DataFrame(causes).to_csv('causes/data/initial_sample.csv') 
    pd.DataFrame(creators).to_csv('creators/data/initial_sample.csv')
    
    print(f"Complete! Collected {len(restaurants)} restaurants, {len(causes)} causes, {len(creators)} creators")

if __name__ == "__main__":
    main()