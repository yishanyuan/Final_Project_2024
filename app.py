import streamlit as st
import pandas as pd
import plotly.express as px

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

# Aggregate data for the world map
country_star_counts = data.groupby(["country", "stars_label"]).size().unstack(fill_value=0)
country_counts = data.groupby("country").size().reset_index(name="Restaurant Count")
country_iso = data[["country", "ISO Code"]].drop_duplicates()
world_data = pd.merge(country_counts, country_iso, on="country", how="left")

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

