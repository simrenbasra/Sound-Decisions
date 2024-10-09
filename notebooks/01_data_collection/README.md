# Data Collection

## Overview

The aim of this project is to build a recommneder for headphones based off products listed on Amazon. 
This folder contains notebooks for data scraping and data cleaning/processing.

## Notebook Summaries

### 1. Data Scrapinf [01-data-scraping.ipynb]

The purpose of this notebook is to scrape 50 pages worth of headphone product data off Amazon: https://www.amazon.co.uk/s?keywords=adult+headphones&i=electronics. The script scrapes the following data from Amazon's search results using BeautifulSoup:

    - product ASIN
    - product description
    - price
    - rating (average user rating)
    - prime eligibility 

### 2. Data Cleaning and Processing [02-data-cleaning.ipynb]


This notebook focuses on cleaning the scraped data as well as applying feature extraction methods on product descriptions to further enhance the data
This involves removing duplicated entries and rows with missing values, in addition to using regular expressions to extract features from product descriptions.

## Outcome

After running these notebooks we have two data diles in CSV form:

- scraped_data.csv : all porducts from 50 pages worth of scraping.
- cleaned_data.csv : cleaned scraped data with extra features from feature extraction.