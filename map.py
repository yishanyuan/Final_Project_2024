import pandas as pd
from code.database import get_engine

def create_map():
    """
    Query statistical data from the database and save it as a CSV file.
    """

    query = """
    SELECT 
        c.iso_code,
        c.country,
        COUNT(*) AS total_michelin,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 0 THEN 1 ELSE 0 END) AS zero_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 1 THEN 1 ELSE 0 END) AS one_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 2 THEN 1 ELSE 0 END) AS two_star,
        SUM(CASE WHEN CAST(c.stars_label AS INTEGER) = 3 THEN 1 ELSE 0 END) AS three_star
    FROM 
        cleaned_data_with_embeddings c
    GROUP BY 
        c.iso_code, c.country
    ORDER BY 
        total_michelin DESC;
    """
    
    engine = get_engine()
    try:
        with engine.connect() as connection:
            data = pd.read_sql(query, connection)

        output_file = "michelin_statistics_by_country.csv"
        data.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        return data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

