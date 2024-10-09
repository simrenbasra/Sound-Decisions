# -----------------------------------------
# Feature Extraction Script
# -----------------------------------------

# -----------------------------------------
# Imports
# -----------------------------------------

import numpy as np
import pandas as pd
import re
import matplotlib
import spacy
from sklearn.preprocessing import OneHotEncoder
# -----------------------------------------
# Extraction Functions
# -----------------------------------------

def search_description(description, regexp):
    '''
    Outputs binary value

    Parameters
    ---------
    description: string of product description
    regexp: regular expression

    Returns
    -------
    1 if regexp is present in description, 0 if not
    '''
    return 1 if re.search(regexp, description.lower()) else 0

def get_colour(description):
    '''
    Outputs colour in product description

    Parameters
    ---------
    description: string of product description

    Returns
    -------
    Colour mentioned in the description
    '''
    colour_names = matplotlib.colors.CSS4_COLORS.keys()
    for colour in colour_names:
        if re.search(rf'\b{colour}\b', description):
            return colour
    return 'Not Specified'

def get_battery_life(description):
    '''
    Outputs battery life listed in product description

    Parameters
    ---------
    description: string of product description

    Returns
    -------
    Battery life in hours
    '''
    regexp = r'(\b[1-9]\d*)\s*(battery|batteries|hours?|hrs?|h)'
    match = re.search(regexp, description)
    return match.group(1) if match else 'Not Specified'


def extract_features(df):
    '''
    Perform feature extraction of product description from given dataframe.

    Parameters
    ---------
    df: Dataframe to get extract features from 

    Returns
    -------
    Dataframe with extra features added
    '''

    # Set description to all lowercase first
    df['Description'] = df['Description'].str.lower()

    # Extract Features using functions above
    df['Wireless'] = df['Description'].apply(search_description, args=(r'\bwireless\b',))
    df['Noise Cancelling'] = df['Description'].apply(search_description, args=(r'\bnoise[-\s]?cancelling\b',))
    df['Colour'] = df['Description'].apply(get_colour)
    df['Battery Life'] = df['Description'].apply(get_battery_life)
    df['Microphone'] = df['Description'].apply(search_description, args=(r'\b(mic?|microphone?)\b',))
    df['Over Ear'] = df['Description'].apply(search_description, args=(r'\b(over[\s-]ear?|overhead?)\b',))
    df['Gaming'] = df['Description'].apply(search_description, args=(r'\bgaming\b',))
    df['Foldable'] = df['Description'].apply(search_description, args=(r'\bfoldable\b',))

    return df


def clean_features(df):

    # Known issue from notebooks
    df['Colour'] = df['Colour'].replace('gray', 'grey')

    df['Battery Life'] = df['Battery Life'].replace('Not Specified', 0)
    df['Battery Life'] = df['Battery Life'].astype(int)

    # Transformation of price
    df['price_trans'] = np.log(df['Price'])

    # Fixing colour
    colours_to_grp = df['Colour'].value_counts() < 10
    df['Colour'] = df['Colour'].replace(colours_to_grp[colours_to_grp].index, 'Other')

    encoder = OneHotEncoder()
    one_hot_encoded = encoder.fit_transform(df[['Colour']])
    colour_df = pd.DataFrame(one_hot_encoded.toarray(),columns = encoder.get_feature_names_out(['Colour']))
    # Step 4: Concatenate the original DataFrame and the one-hot encoded DataFrame
    df_final = pd.concat([df, colour_df], axis=1)

    # Step 5: (Optional) Drop the original 'Colour' column if no longer needed
    df_final = df_final.drop(columns=['Colour', 'Price'])

    return (df_final)

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('../data/post_cleaning.csv', index_col=0)

    # Clean the data
    df_extra_features = extract_features(df)

    # Clean features
    final_df = clean_features(df_extra_features)

    # Export to CSV
    final_df.to_csv('../data/final_df.csv')

