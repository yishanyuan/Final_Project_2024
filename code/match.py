import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path


current_path = Path(__file__).resolve().parent
project_root = current_path.parent  


csv_path = project_root / "artifacts" / "cleaned_data_with_embeddings.csv"


print(f"Resolved CSV path: {csv_path}")


if not csv_path.exists():
    print(f"Error: The file at path '{csv_path}' does not exist.")
    exit()


model = SentenceTransformer("all-MiniLM-L6-v2")


try:
    df = pd.read_csv(csv_path)
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file at path '{csv_path}' does not exist.")
    exit()


df['embedding'] = df['embedding'].apply(eval)

def match(user_query):
    """
    对用户输入生成嵌入，然后计算与每个餐馆描述嵌入的相似性。
    返回最相似的20个独特餐馆信息。
    """
    
    user_embedding = model.encode([user_query])[0]

    
    user_embedding_np = np.array(user_embedding).reshape(1, -1)

    
    embeddings = np.array(df['embedding'].tolist()) 
    
    
    similarities = cosine_similarity(user_embedding_np, embeddings)[0]

    
    df['similarity'] = similarities

    
    print(df[['name', 'similarity']].sort_values(by='similarity', ascending=False))

    
    df_filtered = df[df['similarity'] > 0.5].sort_values(by='similarity', ascending=False)

    
    top_100 = df_filtered.head(100)

    
    unique_restaurants = top_100.drop_duplicates(subset='name').head(20)

    
    data_list = []
    for _, row in unique_restaurants.iterrows():
        data = {
            "UniqueID": row.get("UniqueID", "N/A"),
            "name": row.get("name", "N/A"),
            "address": row.get("address", "N/A"),
            "country": row.get("country", "N/A"),
            "stars_label": row.get("stars_label", "N/A"),
            "ISO Code": row.get("ISO Code", "N/A"),
            "similarity": row.get("similarity", 0.0)
        }
        data_list.append(data)


    if len(data_list) == 0:
        raise Exception("Did not find any results.")
    
    return data_list


if __name__ == "__main__":
    user_query = "A cozy place with great vegetarian food"
    try:
        results = match(user_query)
        for result in results:
            print(result)
    except Exception as e:
        print(e)
