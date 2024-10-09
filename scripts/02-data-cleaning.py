# -----------------------------------------
# Data Cleaning Script
# -----------------------------------------

# -----------------------------------------
# Imports
# -----------------------------------------

import numpy as np
import pandas as pd
import re
import matplotlib
import spacy

def df_check(df):
    '''
    Outputs quality measures for dataframes

    Parameters
    ---------
    df: DataFrame for quality check

    Returns
    -------
    Statements with data quality info such as shape, duplicated values, missing values
    '''
    shape = df.shape
    null_vals = df.isna().sum().sum()
    duplicated_rows = df.duplicated().sum()
    duplicated_cols = df.columns.duplicated().sum()

    print(
        f"""
        Data Quality Checks:
        --------------------------------------------
        No. of rows: {shape[0]}
        No. of columns: {shape[1]}
        No. of missing values: {null_vals}
        No. of duplicated rows: {duplicated_rows}
        No. of duplicated columns: {duplicated_cols}
        """
    )

def clean_data(df):
    '''
    Perform data cleaning on the given df.

    Parameters
    ---------
    df: Dataframe to clean and process

    Returns
    -------
    Cleaned and processed data as a dataframe, ready for EDA
    '''
    # Check initial data quality
    df_check(df)

    # Remove duplicates
    df = df.drop_duplicates()
    df_check(df)

    # Drop rows with missing data
    df = df.dropna()
    df_check(df)

    # Remove 'Not Specified' from Price column
    df = df[df['Price'] != 'Not Specified']
    df['Price'] = df['Price'].str.replace(',', '').astype(float)

    # Clean Rating
    df['Rating'] = df['Rating'].astype('str').str.replace('out of 5 stars', '').astype(float)

    # Reset the index
    df = df.reset_index(drop=True)

    return df

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('../data/post_scrape.csv', index_col=0)

    # Clean the data
    cleaned_df = clean_data(df)

    # Export to CSV
    cleaned_df.to_csv('../data/post_cleaning.csv')

