# -----------------------------------------
# Data Scraping Script
# -----------------------------------------

# -----------------------------------------
# Imports
# -----------------------------------------
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# -----------------------------------------
# Scraping function
# -----------------------------------------
def scrape_headphone_data(base_url, num_pages):
    # To store scraped data
    data = []

    # Loop through the number of pages to scrape
    for page in range(num_pages):

        # Print the current page number being scraped
        print(f"Scraping page {page + 1}...")

        # Construct the URL for the current page
        url = base_url + str(page + 1)
        
        # Define the headers for the GET request to mimic a browser (avoids error)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.5938.62"
        }
        
        # Send a GET request to the URL with the headers
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code = 200)
        if response.status_code == 200:
            # Use BeautifulSoup to 'read' content on page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extracts div storing all search results
            all_headphones = soup.find_all('div', {'data-component-type': 's-search-result'})

            # Loop through each product found to extract product details
            for headphone in all_headphones:
                # Getting product IDs
                if headphone.has_attr('data-asin'):
                    hp_ASIN = headphone['data-asin']
                else:
                    hp_ASIN = 'Not Specified'

                # Getting product descriptions
                desc = headphone.find('span', class_='a-size-medium a-color-base a-text-normal')
                hp_desc = desc.get_text(strip=True) if desc else 'N/A'

                # Getting product price
                price_pound = headphone.find('span', class_='a-price-whole')
                price_pennies = headphone.find('span', class_='a-price-fraction')

                if price_pound and price_pennies:
                    hp_price = price_pound.get_text(strip=True) + (price_pennies.get_text(strip=True))
                else:
                    hp_price = 'Not Specified'
                
                # Get overall rating
                rating = headphone.find('span', class_='a-icon-alt')
                hp_rating = rating.get_text(strip=True) if rating else 'N/A'

                # Check if headphone is prime
                prime = headphone.find('span', class_='aok-relative s-icon-text-medium s-prime')
                is_prime = '1' if prime else '0'

                # Add product info to list
                data.append({
                    'Product ID': hp_ASIN,
                    'Description': hp_desc,
                    'Price': hp_price,
                    'Rating': hp_rating,
                    'Is Prime': is_prime
                })
            
            # Delay by 2 seconds after each page to avoid overwhelming the server
            time.sleep(2)

        else:
            print(f"Failed to access the webpage: {url}")

    # Return the scraped data in a dataframe
    return pd.DataFrame(data)

# Calling the above function
if __name__ == "__main__":
    # Defining params to pass in
    base_url = "https://www.amazon.co.uk/s?keywords=adult+headphones&i=electronics&page="
    num_pages = 50

    # Run function
    headphones_df = scrape_headphone_data(base_url, num_pages)

    # Export results to data file
    headphones_df.to_csv('../data/post_scrape.csv')

