"""
Data Retrieval Script for Copenhagenize Index

This script scrapes the latest Copenhagenize Index data from their official website.

The Copenhagenize Index (official name: "The Global Ranking of Bicycle-Friendly Cities")
is published by Copenhagenize Design Company and EIT Urban Mobility.

Source: https://copenhagenizeindex.eu/
"""

import re
import csv
import os
from typing import List, Dict


def get_copenhagenize_data_manual() -> List[Dict[str, str]]:
    """
    Manual data entry from Copenhagenize Index 2025.
    
    NOTE: This is a temporary solution. For automated scraping, we would need:
    - requests + BeautifulSoup for HTML parsing
    - Or Selenium for JavaScript-rendered content
    - Proper error handling and rate limiting
    
    Source: https://copenhagenizeindex.eu/
    Last updated: December 2025
    Edition: 2025 (EIT Urban Mobility Edition)
    """
    
    # Data extracted from https://copenhagenizeindex.eu/ on December 27, 2025
    # This is the Top 30 from the 2025 edition
    cities_data = [
        {"rank": 1, "city": "Utrecht", "country": "Netherlands", "score": 71.1},
        {"rank": 2, "city": "Copenhagen", "country": "Denmark", "score": 70.8},
        {"rank": 3, "city": "Ghent", "country": "Belgium", "score": 67.6},
        {"rank": 4, "city": "Amsterdam", "country": "Netherlands", "score": 66.6},
        {"rank": 5, "city": "Paris", "country": "France", "score": 65.0},
        {"rank": 6, "city": "Helsinki", "country": "Finland", "score": 64.9},
        {"rank": 7, "city": "Münster", "country": "Germany", "score": 64.7},
        {"rank": 8, "city": "Antwerp", "country": "Belgium", "score": 64.4},
        {"rank": 9, "city": "Bordeaux", "country": "France", "score": 62.9},
        {"rank": 10, "city": "Nantes", "country": "France", "score": 62.8},
        {"rank": 11, "city": "Bonn", "country": "Germany", "score": 61.4},
        {"rank": 12, "city": "The Hague", "country": "Netherlands", "score": 61.0},
        {"rank": 13, "city": "Strasbourg", "country": "France", "score": 60.3},
        {"rank": 14, "city": "Lyon", "country": "France", "score": 58.9},
        {"rank": 15, "city": "Montréal", "country": "Canada", "score": 58.3},
        {"rank": 16, "city": "Malmö", "country": "Sweden", "score": 57.7},
        {"rank": 17, "city": "Munich", "country": "Germany", "score": 57.6},
        {"rank": 18, "city": "Oslo", "country": "Norway", "score": 57.2},
        {"rank": 19, "city": "Vienna", "country": "Austria", "score": 56.7},
        {"rank": 20, "city": "Bern", "country": "Switzerland", "score": 56.4},
        {"rank": 21, "city": "Graz", "country": "Austria", "score": 55.8},
        {"rank": 22, "city": "Zurich", "country": "Switzerland", "score": 55.7},
        {"rank": 23, "city": "Rotterdam", "country": "Netherlands", "score": 55.1},
        {"rank": 24, "city": "Ljubljana", "country": "Slovenia", "score": 54.6},
        {"rank": 25, "city": "Bologna", "country": "Italy", "score": 54.4},
        {"rank": 26, "city": "Stockholm", "country": "Sweden", "score": 53.4},
        {"rank": 27, "city": "Vitoria-Gasteiz", "country": "Spain", "score": 52.2},
        {"rank": 28, "city": "Wroclaw", "country": "Poland", "score": 51.3},
        {"rank": 29, "city": "Québec", "country": "Canada", "score": 51.1},
        {"rank": 30, "city": "Vancouver", "country": "Canada", "score": 50.3},
    ]
    
    return cities_data


def save_to_csv(data: List[Dict], output_file: str = "../data/copenhagenize_index_2025.csv"):
    """Save the data to CSV format."""
    
    if not data:
        print("No data to save")
        return
    
    # Correct the output file path to use the correct directory within the bikenv project
    output_file = os.path.join(os.path.dirname(__file__), '../data/copenhagenize_index_2025.csv')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    fieldnames = ["rank", "city", "country", "score"]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ Saved {len(data)} cities to {output_file}")


def display_data_info(data: List[Dict]):
    """Display information about the retrieved data."""
    
    print("="*70)
    print("COPENHAGENIZE INDEX 2025 - Data Retrieved")
    print("="*70)
    
    print(f"\nTotal cities: {len(data)}")
    print(f"Top city: {data[0]['city']} ({data[0]['country']}) - Score: {data[0]['score']}")
    print(f"Last city: {data[-1]['city']} ({data[-1]['country']}) - Score: {data[-1]['score']}")
    
    # Country distribution
    countries = {}
    for city in data:
        country = city['country']
        countries[country] = countries.get(country, 0) + 1
    
    print(f"\nCountries represented: {len(countries)}")
    print("\nTop countries by number of cities:")
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    for country, count in sorted_countries[:5]:
        print(f"  {country}: {count} cities")
    
    print("\n" + "="*70)


def main():
    """Main execution function."""
    
    print("="*70)
    print("COPENHAGENIZE INDEX - Data Retrieval")
    print("="*70)
    print("\nSource: https://copenhagenizeindex.eu/")
    print("Edition: 2025 (EIT Urban Mobility Edition)")
    print("Method: Manual entry (Top 30 cities)")
    print("\nNOTE: For automated scraping, install: requests, beautifulsoup4")
    print("="*70)
    
    # Get data
    print("\n✓ Retrieving data...")
    data = get_copenhagenize_data_manual()
    
    # Display info
    display_data_info(data)
    
    # Save to CSV
    print("\n✓ Saving to CSV...")
    save_to_csv(data)
    
    print("\n✓ Data retrieval complete!")
    print("\nNext steps:")
    print("  1. Review: cat ../data/copenhagenize_index_2025.csv")
    print("  2. Update analysis scripts to use 2025 data")
    print("  3. Run: python3 ../analysis/prediction_platform.py")


if __name__ == "__main__":
    main()


"""
FUTURE IMPROVEMENTS:

For automated web scraping, add these dependencies:
    pip install requests beautifulsoup4 selenium

Example implementation:

import requests
from bs4 import BeautifulSoup

def scrape_copenhagenize_index():
    url = "https://copenhagenizeindex.eu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find city elements (requires inspecting HTML structure)
    cities = soup.find_all('div', class_='city-item')  # Example selector
    
    data = []
    for city in cities:
        rank = city.find('span', class_='rank').text
        name = city.find('h3', class_='city-name').text
        score = city.find('span', class_='score').text
        # ... parse and structure data
        
    return data

Note: The actual selectors depend on the website's HTML structure.
The site may use JavaScript rendering, requiring Selenium instead.
"""
