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
    "Gaming": st.checkbox("Gaming", value=False)
}

st.markdown("---")

# Slider features
# Tuple for min/max price range
price_range = st.slider("Select Price Range (£)", min_value=df['Price'].min(), max_value=df['Price'].max(), step = 10.0, value=(0.0, df['Price'].max().round()))
min_price_selected, max_price_selected = price_range  

st.markdown("---")

# Slider features
rating = st.slider("Select Minimum Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)

st.markdown("---")

battery_life = st.slider("Select Minimum Battery Life (hours)", min_value=df['Battery Life'].min(), max_value=df['Battery Life'].max(), value=10)

st.markdown("---")

# Multiselect features
colour_columns = [colour_col for colour_col in df.columns if colour_col.startswith('Colour')]
colour_names = [colour.replace('Colour_','') for colour in colour_columns]
# Removing Not Specified as its confusing to users
colour_names.remove('Not Specified')
colours = st.multiselect('Select Colour Preferences', options=colour_names)

st.markdown("---")
#-----------------------------------------
# Filtering of Data
#-----------------------------------------
filtered_df = df.copy()

for feature, selected in features.items():
    if selected:
        filtered_df = filtered_df.loc[filtered_df[feature]==1]

# Filter by Price - need to take log of input price

filtered_df = filtered_df.loc[(filtered_df['Price'] <= max_price_selected) & (filtered_df['Price'] >= min_price_selected)] 

# Filter by Rating
filtered_df = filtered_df.loc[filtered_df['Rating'] >= rating]

# Filter by Battery Life
filtered_df = filtered_df.loc[filtered_df['Battery Life'] >= battery_life]

if colours:
    # using np.any to find rows where any of the selected colours match the user input
    colour_filters = np.any([filtered_df[f'Colour_{colour}'] == 1 for colour in colours],axis=0)
    filtered_df = filtered_df[colour_filters] 

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

    st.markdown("#### Recommended Headphones:")

    # Check if the output is a DataFrame or a string (no products available)
    if isinstance(recommended_products, pd.DataFrame):
       # using to_html to make links clickable
        st.write(recommended_products.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.write(recommended_products)

