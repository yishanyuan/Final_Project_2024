import pandas as pd
import re
import json
import os

# Define relative paths
data_folder = './data'
artifacts_folder = './artifacts'
input_jsonl_path = os.path.join(data_folder, 'results_raw.jsonl')
output_csv_path = os.path.join(artifacts_folder, 'cleaned_data.csv')

# Create artifacts directory if it doesn't exist
os.makedirs(artifacts_folder, exist_ok=True)

# Load the JSONL file
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

# Count the symbol of dollars and catergorize the prices
def count_symbols(price):
    if isinstance(price, str):
        return len(re.findall(r'[^\w\s]', price))
    return 0

df['price_symbol_count'] = df['price'].apply(count_symbols)

# Drop "price" and "stars" columns
df = df.drop(columns=['price', 'stars'], errors='ignore')

# Keep the "facilities_services" column
if 'facilities_services' not in df.columns:
    df['facilities_services'] = None

# Save the cleaned data to CSV
df.to_csv(output_csv_path, index=False)

print(f"Cleaned data saved to {output_csv_path}")
