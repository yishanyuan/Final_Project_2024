import pandas as pd
import geopandas as gpd
import ast
from code.database import get_engine

def query_data():
    query = """
    SELECT name, food_type, address, stars_label, latitude_and_longitude
    FROM cleaned_data_with_embeddings
    WHERE latitude_and_longitude IS NOT NULL;
    """
    engine = get_engine()
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    def extract_lat_lng(value):
        try:
            value_dict = ast.literal_eval(value)
            return value_dict.get('lat'), value_dict.get('lng')
        except (ValueError, SyntaxError, TypeError):
            return None, None

    df['latitude'], df['longitude'] = zip(*df['latitude_and_longitude'].apply(extract_lat_lng))
    df = df.dropna(subset=['latitude', 'longitude'])

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    return gdf

def get_nearest_restaurants(selected_point, gdf, num_results=10):
    gdf['distance'] = gdf.geometry.apply(lambda x: selected_point.distance(x))
    nearest_restaurants = gdf.sort_values('distance').head(num_results)
    return nearest_restaurants
