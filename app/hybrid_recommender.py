import pandas as pd
from sklearn.preprocessing import MinMaxScaler
def hybrid_recommender(df, filtered_df, similarities, alpha=0.6):
    """
    Recommends products based on features (selected by the user) and product ratings.

    Parameters:
    - df: Unfiltered dataframe
    - filtered_df: DataFrame of products filtered by user preferences
    - similarities: Pre-made cosine similarity matrix
    - alpha: Weighting factor for combining feature similarity and rating

    Returns:
    - top_df: DataFrame of top recommended products
    """

    # Check if filtered_df is empty
    if filtered_df.empty:
        return ('No products found matching your preferences. Please adjust filters.')
    
    # Normalising the Rating field for calculation
    scaler = MinMaxScaler()
    df['Normalised Rating'] = scaler.fit_transform(df[['Rating']])

    # Find first product_id of product after filtering
    product_id = filtered_df['Product ID'].iloc[0]  
    product_index = df[df['Product ID'] == product_id].index[0]

    # Use this id to generate recommendations
    cosine_sim = similarities[product_index, :].flatten()

    # Combine similarity score with the ratings from the filtered DataFrame
    combined_score = (alpha * cosine_sim) + ((1 - alpha) * df['Normalised Rating'])

    # Create a DataFrame for the recommended products
    sim_df = pd.DataFrame({
        'Product ID': df['Product ID'],
        'Combined Similarity': combined_score,
        'Rating': df['Rating']
    })

    # Filter and sort to get the top recommendations
    top_df = sim_df.sort_values(by='Combined Similarity', ascending=False).head(6)
    top_df.reset_index(drop=True, inplace=True)

    # Generate URL for easy access to recommended products
    top_df['Product URL'] = 'https://www.amazon.com/dp/' + top_df['Product ID']

    return top_df[['Product ID', 'Rating', 'Product URL']][1:]
