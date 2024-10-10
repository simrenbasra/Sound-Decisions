
# Sound-Decisions: Headphone Recommender System

## Project Overview

### Objective: To create a recommnder system based on products scraped on Amazon.

This project aims to develop a hybrid recommender system for headphones, using both content-based and collaborative filtering methods to generate personalised recommendations. The dataset used in this project was scraped from Amazon, focusing on search result data for adult headphones. Additionally, a Streamlit app was built to allow users to input their preferences and receive tailored headphone recommendations.

## Key Features

- **Data Collection**: Scraped data from Amazon's headphone search results.
- **Data Processing**: Cleaning and feature extraction to enhance the dataset.
- **Hybrid Recommender System**: Building a hybrid recommender combining both content-based  and collaborative filtering methods.
- **Streamlit App**: An interactive app allowing users to input preferences and get recommendations.

## Project Structure

### 1. Data Collection

The `01_data_collection` folder contains notebooks used for scraping headphone product data from Amazon and cleaning the data. The scraping collects the following data: product ASIN, product description, price, rating and Prime eligibility. The cleaning notebook ensures data quality by removing duplicates, dropping missing values and performs feature extraction from product descriptions to enhance the dataset.

### 2. Exploratory Data Analysis (EDA)
The `02_data_eda` folder includes EDA-related notebooks where I get insights into product features, theirdistributions and trends. This section also handles data transformations, such as addressing skewness in pricing and ratings. I also explore various clustering methods to identify groupings of similar headphones in the dataset to try understand the similarities between products in the data.

### 3. Recommender System
The `03_recommendations` folder contains notebooks that implement the recommender system. The hybrid recommender uses cosine similarity between product features and also incorporates product ratings to generate personalised headphone suggestions.

### 4. app
The app folder contains the Python files for the Streamlit application and the recommender system used within the app. The Streamlit app allows users to input their headphone preferences and uses the recommender to generate the top five suggestions tailored to the user's needs.

## Installation Instructions

Follow these steps to set up the project environment and install the necessary dependencies.

### 1. Clone the Repository
To start, clone the repository to your local machine:

    git clone https://github.com/simrenbasra/Sound-Decisions.git

### 2. Navigate to the Project Directory (where the repo was cloned)
    
    E.g:
    cd ~/Desktop/Sound-Decisions

### 3. Install the required packages in an pip/conda envirionment
   
    pip install -r requirements.txt

### 4. Get data from Google Drive link

    Navigate to: https://drive.google.com/file/d/19YhcJcMzh7uzcWrEfkEnAkM5GBhcOG1W/view?usp=sharing and download the data into data folder.

### 5. Run the Streamlit App 

    streamlit run app/app.py

    App should open in browser after running command in terminal/bash

## Blog Post

For a more in-depth discussion of this project, including the challenges faced and insights gained, you can read my blog post:

[Sound Decisions: Data Scraping and Cleaning 🎧](https://simrenbasra.github.io/simys-blog/2024/09/25/sound_decisions_part1.html)

[Sound Decisions: EDA 🔍](https://simrenbasra.github.io/simys-blog/2024/10/03/sound_decisions_part2.html)

[Sound Decisions: Recommender System 🧩](https://simrenbasra.github.io/simys-blog/2024/10/11/sound_decisions_part3.html)

## Challenges of the Project

1. Data Limitations from Scraping:

    - A lack of user data in the scraped dataset.
    - Limited to extracting features only from product descriptions due to robots.txt restrictions.
    - Descriptions were often inconsistent which complicated the extraction of information using regular expressions.
    - Consideration of using more complex NLP methods for better results.

2. Real-World Data Challenges:

    - Scraping resulted in messy datasets requiring extensive cleaning and preprocessing.
    - Nearly half of the dataset had missing average user ratings.
    - Decision to drop rows with missing values to avoid bias and preserve data authenticity likely limited the variety of headphones.

3. Deployment Challenges with Streamlit:

    - Attempts to deploy the app publicly using Streamlit and GitHub workflows were unsuccessful.
    - Goal was to make the web app accessible without requiring users to clone the entire project.
    - Future investigation of Flask or FastAPI for better deployment practices.

## Future Work

1. Feedback Loop:

    - Implement a feedback loop to refine recommendations based on user interactions.
    - Collect data on user likes/dislikes regarding recommended products.
    - Build user profiles to allow the recommender to learn and adapt to user preferences more effectively.
    
2. Connecting to the Amazon API:

    - Explore the possibility of connecting to Amazon's API to gather additional headphone information, such as images or detailed descriptions.