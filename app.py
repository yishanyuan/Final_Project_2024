import streamlit as st
import pandas as pd
import plotly.express as px
from code.gis_utils import query_data
from code.match_sql import RestaurantMatcher  # Import the RestaurantMatcher class
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

# Database connection settings
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "pumpkinpie"
DATABASE_HOST = "34.57.167.81"
DATABASE_PORT = "5432"
DATABASE_DATABASE = "finalproject2024"
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DATABASE}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Helper function to run SQL queries
def run_query(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

# Set Streamlit page configuration for full-width layout
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("artifacts/cleaned_data_with_embeddings.csv")

data = load_data()

# Add a title and description
st.markdown("<h1 style='text-align: center;'>Michelin Restaurant Finder 🌍</h1>", unsafe_allow_html=True)
st.write("Search Michelin restaurants using filters or an AI-powered query box.")

# Load the data for the map
try:
    print("Running map.py to fetch the latest Michelin data...")
    subprocess.run(["python3", "map.py"], check=True)
except Exception as e:
    st.error(f"Error occurred while running map.py: {e}")
    st.stop()

csv_file = "michelin_statistics_by_country.csv"
if not os.path.exists(csv_file):
    st.error(f"Error: {csv_file} not found. Ensure map.py ran successfully.")
    st.stop()

data = pd.read_csv(csv_file)

# Debug: Print unique country names
print("Unique country names in dataset:", data["country"].unique())

# Add hover text with details for each country
hover_texts = []
for _, row in world_data.iterrows():
    country = row["country"]
    hover_text = f"<b>{country}</b><br>Total Restaurants: {row['Restaurant Count']}<br>"
    if country in country_star_counts.index:
        star_counts = country_star_counts.loc[country].to_dict()
        for star, count in star_counts.items():
            hover_text += f"{star} Stars: {count}<br>"
    hover_texts.append(hover_text)

world_data["hover_text"] = hover_texts

# Create a full-width world map using Plotly
fig = px.choropleth(
    world_data,
    locations="ISO Code",
    color="Restaurant Count",
    hover_name="country",
    hover_data={
        "Restaurant Count": True,  
        "ISO Code": False,  
    },
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Number of Michelin Restaurants by Country",
)

# layout for fullscreen map
fig.update_geos(
    showcoastlines=True, 
    coastlinecolor="LightGrey", 
    showframe=False,
    projection_type="natural earth",
)

fig.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),  
    coloraxis_colorbar=dict(
        title="Restaurant Count",
        ticks="outside",
    ),
)

# Fix hover template to display the hover text
fig.update_traces(
    hovertemplate="%{customdata}<extra></extra>",  
    customdata=world_data["hover_text"],  
)

# Display the full-screen world map
st.plotly_chart(fig, use_container_width=True)

# Dropdown filters
st.write("### Filter Michelin Restaurants")
star_options = ["All"] + sorted(data["stars_label"].astype(str).unique())
country_options = ["All"] + sorted(data["country"].unique())
cuisine_options = ["All"] + sorted(data["food type"].dropna().unique())

selected_star = st.selectbox("Select Star Rating:", star_options)
selected_country = st.selectbox("Select Country:", country_options)
selected_cuisine = st.selectbox("Select Cuisine Type:", cuisine_options)
selected_price = st.slider("Select Price Range (0 = Cheapest, 4 = Most Expensive):", 0, 4, (0, 4))

# Build SQL query based on filters
query = """
SELECT name AS "Restaurant Name", 
       food_type AS "Cuisine", 
       country AS "Country", 
       stars_label AS "Star Rating",
       CAST(price_symbol_count AS INTEGER) AS "Price Range",
       description
FROM cleaned_data_with_embeddings
WHERE 1=1
"""
params = {}

if selected_star != "All":
    filtered_data = filtered_data[filtered_data["stars_label"].astype(str) == selected_star]
if selected_country != "All":
    filtered_data = filtered_data[filtered_data["country"] == selected_country]
if selected_cuisine != "All":
    query += " AND food_type = :food_type"
    params["food_type"] = selected_cuisine
query += " AND CAST(price_symbol_count AS INTEGER) BETWEEN :min_price AND :max_price"
params["min_price"], params["max_price"] = selected_price

# Run the filtered query
filtered_data = run_query(query, params=params)

# Prepare data for display
filtered_data = filtered_data[["Restaurant Name", "Cuisine", "Country", "Star Rating", "Price Range"]]
filtered_data.reset_index(drop=True, inplace=True)
filtered_data.index += 1  # Start index from 1
filtered_data.index.name = "No."

# Display the data with a wide format
st.write("### Filtered Results")
if filtered_data.empty:
    st.write("No restaurants match the selected filters.")
else:
    st.dataframe(filtered_data, use_container_width=True)

# AI-Powered Restaurant Search
st.write("### Combined AI and Keyword Search")
matcher = RestaurantMatcher()  # Initialize the RestaurantMatcher
ai_query = st.text_input("Enter a query to find restaurants (e.g., 'cozy Italian bistro with pasta' or keywords like 'Cantonese'):")

if ai_query:
    try:
        st.write("Running AI-based search...")
        ai_results = matcher.match(ai_query)  # Use the match method
        ai_results_df = pd.DataFrame(ai_results)
        ai_results_df = ai_results_df[
            ["name", "address", "country", "stars_label", "iso_code", "similarity"]
        ]
        ai_results_df.rename(
            columns={
                "name": "Restaurant Name",
                "address": "Address",
                "country": "Country",
                "stars_label": "Star Rating",
                "iso_code": "ISO Code",
                "similarity": "Similarity Score",
            },
            inplace=True,
        )
        st.write("### AI Search Results")
        st.dataframe(ai_results_df, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
