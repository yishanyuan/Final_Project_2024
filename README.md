# Sentence-Transformers and Pgvector

## Embedding

Using the `python3 code/embedding.py` on the cmd to run the data.

### **Key Functions:**<br>
`load_model`: Load the pre-trained `all-MiniLM-L6-v2` model to generate text embeddings.<br>

`load_csv`: Load the `cleaned_data.csv` file from the artifacts directory and ensure the file exists.<br>

`validate_column`: Check whether the specified description column exists in the DataFrame loaded from `cleaned_data.csv`.<br>

`generate_embeddings`: Generate sentence embeddings for the description column in `cleaned_data.csv` using the `all-MiniLM-L6-v2` model and store them in a new column named `embedding`.<br>

`save_csv`: Save the updated DataFrame, including the new embedding column, to the `cleaned_data_with_embeddings.csv` file in the artifacts directory.<br>

`process_csv_with_embeddings`: Integrate all steps to load `cleaned_data.csv`, validate its structure, generate embeddings for the description column, and save the processed file as `cleaned_data_with_embeddings.csv` in the artifacts directory.<br>

### **Description：**<br>
This script is designed to process textual data from a CSV file and enhance it with sentence embeddings using a pre-trained model. It begins by loading the `all-MiniLM-L6-v2` model, which specializes in generating embeddings for text descriptions. <br>

Next, it reads the `cleaned_data.csv` file from the `artifacts` directory, ensuring the file exists before proceeding. Once the file is loaded, the script validates that the necessary `description` column is present in the dataset, as this column contains the text data to be processed. For each entry in the `description` column, the script generates a sentence embedding using the loaded model and stores the results in a new column named `embedding`. <br>

After processing all rows, the updated data is saved to a new file, `cleaned_data_with_embeddings.csv`, in the same `artifacts` directory. The entire process, from loading the file to saving the enhanced data, is streamlined through a single function, ensuring the workflow is both efficient and easy to manage.

## Match SQL with pgvector

Using the python3 code/match_sql.py on the cmd to run the matching logic.

### **Key Functions:** <br>

`__init__`: Initialize the `RestaurantMatcher` class by setting up a database connection with `SQLAlchemy` and loading the `all-MiniLM-L6-v2` model for text embeddings.<br>

`match`: Generate an embedding for the user query and use `pgvector` in the database to find the top 20 restaurants with similar embeddings. The similarity is calculated using cosine distance, and results are filtered to include only restaurants with a similarity score above 0.5. This function queries the database table `cleaned_data_with_embeddings`.<br>

`update_embeddings`: Calculate new embeddings for the descriptions in the CSV file `cleaned_data.csv` (stored in the artifacts directory) and update the `cleaned_data_with_embeddings` table in the database with the new embeddings.<br>

`run_match_query`: Execute the match function with a user query, handle potential exceptions, and print the matching results.<br>

### **Description：**<br>
This script enables efficient restaurant matching based on textual similarity, using a combination of sentence embeddings and database queries. It begins by initializing the RestaurantMatcher class, which sets up the required `SQLAlchemy` engine and loads the `all-MiniLM-L6-v2` model for embedding generation.

The core functionality is provided by the match method, which takes a user query as input, generates a sentence embedding, and queries a PostgreSQL database equipped with `pgvector`. This query returns the top 20 restaurants from the `cleaned_data_with_embeddings` table with the highest similarity scores, provided the similarity is above 0.5. The results include essential restaurant details like uniqueid, name, address, country, stars_label, and similarity.

Additionally, the update_embeddings function allows updating the embeddings in the `cleaned_data_with_embeddings` table with new data from the CSV file `cleaned_data.csv`, ensuring the system stays current. For ease of use, the `run_match_query` function integrates the matching logic and prints the results, making it convenient to test or use interactively. The entire workflow is optimized for matching restaurants based on user input with high accuracy and relevance.
