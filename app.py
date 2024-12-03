import streamlit as st
import pandas as pd
import plotly.express as px
from huggingface_hub import hf_hub_download
from code.match import match

# Set Streamlit page configuration for wide layout
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("artifacts/cleaned_data_with_embeddings.csv")

data = load_data()

# Add a title and description
st.markdown("<h1 style='text-align: left;'>Michelin Restaurant Finder 🌍</h1>", unsafe_allow_html=True)
st.write("Click on a country to see the total number of Michelin restaurants and their breakdown by star ratings.")

