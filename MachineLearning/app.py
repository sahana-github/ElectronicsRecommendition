import streamlit as st
import pickle
import pandas as pd

# Load data once at the start for efficiency
similarity = pickle.load(open('similarity.pkl', 'rb'))
files = pickle.load(open('files.pkl', 'rb'))
file = pd.DataFrame(files)

def get_recommendations(title):
    """
    Get a list of recommended items based on similarity to the provided title.
    
    Args:
    title (str): The title of the item to base recommendations on.
    
    Returns:
    list: A list of recommended item titles.
    """
    try:
        # Find the index of the item
        item_index = file[file['Title'] == title].index[0]
        # Get similarity distances
        distances = similarity[item_index]
        # Enumerate and sort the distances, skipping the first item (itself)
        item_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        # Get the titles of the recommended items
        recommendations = [file.iloc[i[0]].Title for i in item_list]
        return recommendations
    except IndexError:
        # Handle case where the title is not found
        return ["Item not found"]

# Streamlit UI
st.title("Electronic Recommendation System")

option = st.selectbox(
    'Select an item to get recommendations:',
    file['Title'].tolist()
)

if st.button('Recommend'):
    recommendations = get_recommendations(option)
    for rec in recommendations:
        # Get the row for the recommended item
        rec_row = file[file['Title'] == rec].iloc[0]
        st.write(rec)
        if 'Image' in rec_row and pd.notna(rec_row['Image']):
            st.image(rec_row['Image'])
