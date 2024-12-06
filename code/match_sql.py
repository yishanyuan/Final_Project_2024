import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

class RestaurantMatcher:
    def __init__(self):
        load_dotenv()
        
        self.DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "pumpkinpie")
        self.DATABASE_HOST = os.getenv("DATABASE_HOST", "34.57.167.81")
        self.DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
        self.DATABASE_DATABASE = os.getenv("DATABASE_DATABASE", "finalproject2024")

        self.DATABASE_URL = f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_DATABASE}"
        self.engine = create_engine(self.DATABASE_URL)

        self._initialize_database()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _initialize_database(self):
        """
        Initializes the database by creating necessary extensions if they do not exist.
        """
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    def match(self, user_query):
        """
        Calculate the application vector of the user's input, then use pgvector to query the database for similar application vectors, returning the top 20 most similar restaurants.
        """
        user_embedding = self.model.encode([user_query])[0]
        user_embedding_list = user_embedding.tolist()  
        user_embedding_string = str(user_embedding_list)

        query = """
            SELECT DISTINCT r.uniqueid, r.name, r.address, r.country, r.stars_label, r.iso_code,
                   1 - (r.embedding <=> :user_embedding_string) AS similarity
            FROM cleaned_data_with_embeddings r
            WHERE (1 - (r.embedding <=> :user_embedding_string)) > 0.5
            ORDER BY similarity DESC
            LIMIT 20
        """

        with self.engine.connect() as conn:
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

    def update_embeddings(self, csv_path):
        """
        Updates the database table with new embeddings calculated from the descriptions in the provided CSV file.
        """
        df = pd.read_csv(csv_path)
        df['embedding'] = df['description'].apply(lambda x: self.model.encode(x).tolist()) 
        df.to_sql('cleaned_data_with_embeddings', con=self.engine, if_exists='replace', index=False)

    def run_match_query(self, user_query):
        """
        Runs the match method and prints the results.
        """
        try:
            results = self.match(user_query)
            for result in results:
                print(result)
        except Exception as e:
            print(e)
