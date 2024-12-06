import pandas as pd
from sqlalchemy import create_engine

# Database connection settings
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "pumpkinpie"
DATABASE_HOST = "34.57.167.81"
DATABASE_PORT = "5432"
DATABASE_DATABASE = "finalproject2024"
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DATABASE}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SQL query to aggregate data
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

# Execute query and save results to CSV
try:
    with engine.connect() as connection:
        # Fetch data
        data = pd.read_sql(query, connection)

    # Optional: Standardize country names
    data["country"] = data["country"].replace({
        "United States of America": "United States",
        "Russia": "Russian Federation",
        # Add other mappings if needed
    })

    # Save results to a CSV file
    output_file = "michelin_statistics_by_country.csv"
    data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
except Exception as e:
    print("Error occurred:", e)
