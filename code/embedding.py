import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path


current_path = Path(__file__).resolve().parent  
project_root = current_path.parent  


csv_path = project_root / "artifacts" / "cleaned_data.csv"
output_csv_path = project_root / "artifacts" / "cleaned_data_with_embeddings.csv"


if csv_path.exists():
    print("File exists. Proceeding to load the CSV.")
else:
    print(f"File does not exist at path: {csv_path}")
    exit()


model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully.")


try:
    df = pd.read_csv(csv_path)
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print(f"The specified file does not exist at path: {csv_path}")
    exit()


print(df.head())


if 'description' not in df.columns:
    print("The 'description' column does not exist in the CSV file.")
    exit()


df["embedding"] = None


print("Generating embeddings for each description...")
for index, row in df.iterrows():
    description = row["description"]
    if pd.notna(description):
        embedding = model.encode(description).tolist()
        df.at[index, "embedding"] = str(embedding)

print("Embeddings generated successfully.")


df.to_csv(output_csv_path, index=False)
print(f"Updated CSV file saved at: {output_csv_path}")
