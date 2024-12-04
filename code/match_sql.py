import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "pumpkinpie")
DATABASE_HOST = os.getenv("DATABASE_HOST", "34.57.167.81")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_DATABASE = os.getenv("DATABASE_DATABASE", "finalproject2024")

DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DATABASE}"
engine = create_engine(DATABASE_URL)


with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


model = SentenceTransformer("all-MiniLM-L6-v2")


def match(user_query):
    """
    Calculate the application vector of the user's input, then use pgvector to query the database for similar application vectors, returning the top 20 most similar restaurants.
    """
    
    user_embedding = model.encode([user_query])[0]
    user_embedding_list = user_embedding.tolist()  
    user_embedding_string = str(user_embedding_list)  

    
    query = """
        SELECT DISTINCT r.uniqueid, r.name, r.address, r.country, r.stars_label, r.iso_code,
               1 - (r.embedding <=> :user_embedding_string) AS similarity
        FROM cleaned_data_with_embeddings r
        WHERE 1 - (r.embedding <=> :user_embedding_string) > 0.5
        ORDER BY similarity DESC
        LIMIT 20
    """

    
    with engine.connect() as conn:
        stmt = text(query)
        result = conn.execute(stmt, {"user_embedding_string": user_embedding_string})

    
    if result.rowcount == 0:
        raise Exception("Did not find any results.")
    else:
        rows = result.fetchall()
        data_list = []
        for row in rows:
            data = {
                "uniqueid": row[0],
                "name": row[1],
                "address": row[2],
                "country": row[3],
                "stars_label": row[4],
                "iso_code": row[5],
                "similarity": row[6],
            }
            data_list.append(data)

    return data_list


if __name__ == "__main__":
    user_query = "A cozy place with great vegetarian food"
    try:
        results = match(user_query)
        for result in results:
            print(result)
    except Exception as e:
        print(e)




def update_embeddings(csv_path):
    df = pd.read_csv(csv_path)
    df['embedding'] = df['description'].apply(lambda x: model.encode(x).tolist()) 
    df.to_sql('cleaned_data_with_embeddings', con=engine, if_exists='replace', index=False)
