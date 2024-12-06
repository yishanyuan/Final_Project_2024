import subprocess
import streamlit as st
import pandas as pd
import plotly.express as px
from code.gis_utils import query_data, get_nearest_restaurants
from code.match_sql import RestaurantMatcher  # Import the RestaurantMatcher class
from dotenv import load_dotenv
import folium
from shapely.geometry import Point
from streamlit_folium import st_folium
import os
from sqlalchemy import create_engine, text

# 加载环境变量
load_dotenv()

DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DATABASE}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Helper function to run SQL queries
def run_query(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

# Set Streamlit page configuration for full-width layout
st.set_page_config(layout="wide")

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

# Prepare data for the world map
hover_texts = []
for _, row in data.iterrows():
    hover_text = f"<b>{row['country']}</b><br>Total Restaurants: {row['total_michelin']}<br>"
    hover_text += f"0 Stars: {row['zero_star']}<br>"
    hover_text += f"1 Star: {row['one_star']}<br>"
    hover_text += f"2 Stars: {row['two_star']}<br>"
    hover_text += f"3 Stars: {row['three_star']}<br>"
    hover_texts.append(hover_text)

data["hover_text"] = hover_texts

# Create the choropleth map
fig = px.choropleth(
    data,
    locations="country",  # Use country names
    locationmode="country names",  # Specify that we are using country names
    color="total_michelin",
    hover_name="country",
    hover_data={
        "total_michelin": True,
        "country": False,
    },
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Number of Michelin Restaurants by Country",
)

# Layout for fullscreen map
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

# Update hover template to display custom hover text
fig.update_traces(
    hovertemplate="%{customdata}<extra></extra>",
    customdata=data["hover_text"],
)

# Display the full-screen world map
st.plotly_chart(fig, use_container_width=True)

# Dropdown filters
st.write("### Filter Michelin Restaurants")

# Fetch unique options for filters from the database
@st.cache_data
def get_filter_options():
    query = """
    SELECT DISTINCT stars_label, country, food_type
    FROM cleaned_data_with_embeddings
    """
    data = run_query(query)
    star_options = ["All"] + sorted(data["stars_label"].astype(str).unique())
    country_options = ["All"] + sorted(data["country"].dropna().unique())
    cuisine_options = ["All"] + sorted(data["food_type"].dropna().unique())
    return star_options, country_options, cuisine_options

# Get filter options
star_options, country_options, cuisine_options = get_filter_options()

# Add filter widgets
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
    query += " AND stars_label = :stars_label"
    params["stars_label"] = selected_star
if selected_country != "All":
    query += " AND country = :country"
    params["country"] = selected_country
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

# Display the filtered data
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




# --- Section 3: GIS交互式地图 ---
def interactive_map():
    st.write("### Interactive Map with Nearest Restaurants")

    # 查询 PostGIS 数据
    gdf = query_data()

    # 创建地图
    map_center = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # 添加餐厅标记
    for _, row in gdf.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"{row['name']} ({row['stars_label']} stars)<br>{row['food_type']}<br>{row['address']}",
        ).add_to(m)

    # 显示地图
    map_data = st_folium(m, width=800, height=600)

    # 寻找最近的餐厅
    if map_data["last_clicked"] is not None:
        clicked_point = Point(map_data["last_clicked"]["lng"], map_data["last_clicked"]["lat"])
        nearest_restaurants = get_nearest_restaurants(clicked_point, gdf)

        st.write("### Nearest Restaurants")
        st.table(
            nearest_restaurants[['stars_label', 'name', 'food_type', 'address']].sort_values(by='stars_label', ascending=False)
        )
interactive_map()