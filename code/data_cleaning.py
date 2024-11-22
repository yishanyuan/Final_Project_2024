import pandas as pd
import re
import json
import os

# Define relative paths
artifacts_folder = './artifacts'
data_folder = './data'
input_jsonl_path = os.path.join(data_folder, 'raw_results.json')
iso_country_codes_path = os.path.join(artifacts_folder, 'iso_country_codes.csv')
output_clean_data_path = os.path.join(artifacts_folder, 'cleaned_data.csv')

# Create artifacts directory if it doesn't exist
os.makedirs(artifacts_folder, exist_ok=True)

# Step 1: Load the JSONL file and generate clean_data.csv
data = []
with open(input_jsonl_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Convert to DataFrame
df = pd.DataFrame(data)

# Clean "name" column: remove weird symbols
df['name'] = df['name'].apply(lambda x: re.sub(r'[^\w\s]', '', x) if isinstance(x, str) else x)

# Clean "address" column: keep text only
df['address'] = df['address'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x) if isinstance(x, str) else x)

# Add "country" column based on the address (assumes country is the last part of the address)
df['country'] = df['address'].apply(lambda x: x.split()[-1] if isinstance(x, str) else None)

# Clean "description" column: keep text only
df['description'] = df['description'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x) if isinstance(x, str) else x)

# Add "stars_label" column: extract the first two words to determine the label
def extract_stars_label(stars):
    if isinstance(stars, str):
        if stars.startswith("Three Stars"):
            return 3
        elif stars.startswith("Two Stars"):
            return 2
        elif stars.startswith("One Star"):
            return 1
        elif stars.startswith("Bib"):
            return 0
    return None

df['stars_label'] = df['stars'].apply(extract_stars_label)

# Drop "price" and "stars" columns
df = df.drop(columns=['price', 'stars'], errors='ignore')

# Save intermediate clean_data.csv
df.to_csv(output_clean_data_path, index=False)

# Step 2: Replace the country column with corrected names and map to ISO codes
iso_country_codes = pd.read_csv(iso_country_codes_path)

# Map the "country" column in cleaned_data to the "Country" column in iso_country_codes
country_to_iso = dict(zip(iso_country_codes['Country'], iso_country_codes['ISO Code']))

# Define a mapping for unmapped countries
unmapped_countries = {
    "Mainland": "China",
    "Kong": "Hong Kong",
    "Dhabi": "United Arab Emirates",
    "Dubai": "United Arab Emirates",
    "Kingdom": "United Kingdom",
    "Korea": "Korea, Republic of",
    "Macau": "Macao",
    "Netherlands": "Netherlands, Kingdom of the",
    "Repblic": "Czechia",
    "Trkiye": "TÃ¼rkiye",
    "USA": "United States of America",
    "Vietnam": "Viet Nam",
}

# Update the country column in df for unmapped countries
df['country'] = df['country'].replace(unmapped_countries)

# Map the ISO Code using the updated country column
df['ISO Code'] = df['country'].map(country_to_iso)

# Add a unique index as the first column
df.reset_index(inplace=True)
df.rename(columns={"index": "UniqueID"}, inplace=True)

# Save the final cleaned data with ISO Code
df.to_csv(output_clean_data_path, index=False)

print(f"Final cleaned data with ISO codes saved to {output_clean_data_path}")
