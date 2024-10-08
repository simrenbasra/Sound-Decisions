import streamlit as st
import pandas as pd
import numpy as np
import joblib
from hybrid_recommender import hybrid_recommender

#-----------------------------------------
# Data Loading
#-----------------------------------------
df = pd.read_csv('../data/final_data.csv', index_col = 0)

cosine_sim = joblib.load('../model/cosine_similarity_matrix.joblib')

if 'product_feedback' not in st.session_state:
    st.session_state.product_feedback = []
#-----------------------------------------
# Title of App
#-----------------------------------------
st.title('Sound Decisions: Headphone Recommender')

st.write('Are you on the hunt for the perfect pair of headphones? Sound Decisions helps you discover the best headphones tailored to your preferences.')
st.write('Simply select your desired features below and scroll dopwn to the recommended the top-rated headphones based on your preferences.')

#-----------------------------------------
# User Inputs(Preferences)
#-----------------------------------------

st.markdown("### **Desired Headphone Features**")

st.text("") 

# Checkbox features
features = {
    "Is Prime": st.checkbox("Is Prime", value=False),
    "Wireless": st.checkbox("Wireless", value=False),
    "Noise Cancelling": st.checkbox("Noise Cancelling", value=False),
    "Microphone": st.checkbox("Microphone", value=False),
    "Foldable": st.checkbox("Foldable", value=False),
    "Over Ear": st.checkbox("Over-Ear", value=False),
}

st.markdown("---")

# Slider features
rating = st.slider("Select Minimum Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)

st.markdown("---")

battery_life = st.slider("Select Minimum Battery Life (hours)", min_value=0, max_value=100, value=10)

st.markdown("---")

# Multiselect features
colour_columns = [colour_col for colour_col in df.columns if colour_col.startswith('Colour')]
colour_names = [colour.replace('Colour_','') for colour in colour_columns]
colours = st.multiselect("Select Color Preferences", options=colour_names, default='Not Specified')

st.markdown("---")
#-----------------------------------------
# Filtering of Data
#-----------------------------------------
filtered_df = df.copy()

for feature, selected in features.items():
    if selected:
        filtered_df = filtered_df.loc[filtered_df[feature]==1]

# Filter by Rating
filtered_df = filtered_df.loc[filtered_df['Rating'] >= rating]

# Filter by Battery Life
filtered_df = filtered_df.loc[filtered_df['Battery Life'] >= battery_life]

if colours:
    for colour in colours:
        colour_column = f'Colour_{colour}'
        filtered_df = filtered_df[filtered_df[colour_column] == 1]

#-----------------------------------------
# Get Recommendations
#-----------------------------------------
st.header('Get Recommendations')

st.write('***Disclaimer:*** Please note that some product links may no longer be available if the product\'s ASIN has changed or the item has been removed from Amazon.')

alpha = st.slider("Select Alpha Paramater", min_value=0.0, max_value=1.0, value=0.6, step=0.1)
st.write("Alpha controls the recommendation balance:")
st.write("1.0 - Recommendations based entirely on product features.")
st.write("0.0 - Recommendations based entirely on average product rating.")

if st.button("Get Recommendations"):
    recommended_products = hybrid_recommender(df,filtered_df, cosine_sim, alpha)

    st.write("Recommended Products:")
    st.write(recommended_products)

