import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import ast

# PostgreSQL connection parameters
db_params = {
    "dbname": "finalproject2024",
    "user": "postgres",
    "password": "pumpkinpie",
    "host": "34.57.167.81",
    "port": "5432"
}

# Function to create connection to PostgreSQL
def get_database_connection():
    engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}")
    return engine

# Function to query data from the database
def query_data():
    engine = get_database_connection()
    query = """
    SELECT name, latitude_and_longitude
    FROM cleaned_data_with_embeddings
    WHERE latitude_and_longitude IS NOT NULL; 
    """
    df = pd.read_sql(query, engine)

    # Extract latitude and longitude from the 'latitude and longitude' column
    def extract_lat_lng(value):
        try:
            # Assuming 'latitude and longitude' is stored as a string dictionary
            value_dict = ast.literal_eval(value)
            return value_dict.get('lat'), value_dict.get('lng')
        except (ValueError, SyntaxError, TypeError):
            return None, None

    df['latitude'], df['longitude'] = zip(*df['latitude_and_longitude'].apply(extract_lat_lng))

    # Drop rows with missing latitude or longitude
    df = df.dropna(subset=['latitude', 'longitude'])

    # Convert DataFrame to GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    return gdf

# Example usage
if __name__ == "__main__":
    gdf = query_data()
    print(gdf.head())
