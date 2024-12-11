# Michelin Guide: Vector-Based Dining Finder
### Group Name: Pumpkin Pie

# Goal of the project
Are you tired of endless scrolling through reviews to find the fine dining experience? Our Michelin Guide: Vector-Based Dining Finder is designed to revolutionize the way you discover restaurants. By leveraging vector embeddings and similarity search, our tool transforms random user queries, like "truffle pasta with outdoor seating," into precise recommendations. Our project focuses on creating a vector database of Michelin-starred restaurants and reviews, coupled with an interactive dashboard to streamline the restaurant discovery process.

# Source of dataset
Michelin Offical Websites: https://guide.michelin.com/us/en

# Scrape Data
Using the `python3 code/scrape.py` on the cmd to run the data.


## Search For Michelin Listings and Save Links

**Key Functions:** <br>
`open`: Initialize the headless browser using `Selenium` WebDriver with customized options.<br>
`search`: Simulate an Airbnb search with specific parameters (location, check-in, check-out dates, and guest details) and extracts property links from the results.<br>
`save_urls`: Save the extracted property links to a JSON file.<br>

**Processing Logic:**
The program begins by launching a headless browser using the `Selenium` WebDriver. It searches for property listings based on the specified cities and check-in/check-out dates. The HTML content of each page is parsed with `BeautifulSoup` to extract property links containing "/rooms/". This process is repeated across all available pages by clicking the "Next" button until no more results are found. Finally, the extracted property links are saved to a JSON file.


## Extract and Save Room Details

**Key Functions:** <br>
`load_urls`: Load saved property links from a JSON file.<br>
`get_room_details_page`: Load and parse the room details page using `BeautifulSoup`.<br>
`extract_room_features`, `extract_price_info`, `extract_house_rules`: Extract room features, pricing details, and house rules respectively from each property page.<br>
`save_to_json`: Save the extracted room details into a JSON file.<br>
`close`: Close the `Selenium` WebDriver once all operations are completed.<br>

**Processing Logic:**
 Load property links from a JSON file. For each link, the corresponding page is opened, and details such as room features, prices, and house rules are extracted. The extracted information is then saved to a JSON file. Once the extraction process is complete, the browser is closed.


# Clean Data

Using the `python3 code/cleaned_data.py` on the cmd to run the data.

**Key Functions:**<br>

'load_jsonl_data': Load the input JSONL file containing raw restaurant data into a pandas DataFrame for processing.
'clean_name_column': Remove non-alphanumeric characters from the restaurant names to ensure consistency.
'extract_country_from_address': Parse the address column to extract the country information, assuming the last word in the address represents the country.
'fix_encoding_issues': Correct improperly encoded text, such as "TÃ¼rkiye," by re-encoding it into the proper UTF-8 format.
'add_stars_label': Generate a numeric column that maps Michelin star ratings to corresponding numeric labels (e.g., "Three Stars" → 3).
'count_price_symbols': Calculate the number of special symbols in the price column to approximate price categories.
'drop_unnecessary_columns': Remove redundant columns such as raw "price" and "stars" to streamline the dataset.
'save_cleaned_data_to_csv': Save the cleaned DataFrame to a CSV file for subsequent SQL ingestion.

**Description**

The clean data process was a critical step in ensuring the accuracy and usability of our Michelin Guide Dining Finder. This stage involved transforming raw data into a structured, clean dataset that could be effectively used for analysis and recommendation generation.

We began by loading a raw dataset in JSONL format and converted it into a tabular format using Python's pandas library. This transformation enabled us to systematically clean and preprocess key columns. For instance, the "name," "address," and "description" columns were stripped of non-alphanumeric characters to ensure consistency. To derive meaningful insights, we also extracted additional features such as "country," which was inferred from the last part of the address field, and "stars_label," which classified restaurants based on Michelin ratings (e.g., Three Stars, Two Stars).

During the process, we noticed inconsistencies in character encoding, particularly for certain country names such as "TÃ¼rkiye," which should be represented as "Türkiye." This issue was addressed by implementing a character encoding correction function that re-encoded problematic text into the proper UTF-8 format. Additionally, unmapped country names were manually corrected and aligned with their corresponding ISO standard names.

To further enhance usability, we implemented a mapping system to link countries with their ISO codes. This was achieved by leveraging an external ISO country codes dataset. For countries that were not directly matched, we created a dictionary of manual mappings to ensure full coverage. The final dataset included a new column for ISO codes, providing a standardized reference for country information.

Lastly, we added an identifier column to uniquely label each restaurant and dropped redundant fields, such as raw price and stars columns, to streamline the dataset. The final cleaned data was saved as a CSV file, ready to be utilized for vector embedding generation and cosine similarity analysis.

This clean data process was instrumental in transforming raw, unstructured data into a robust foundation for the Michelin Guide Dining Finder, ensuring accurate and efficient performance of the recommendation system.

## SQL Table and Extension ##

Copy the codes in create_table.sql to DBeaver to run the sql codes. 

**Key Functions:**<br>

'upload_to_postgresql': Upload the cleaned CSV file to a PostgreSQL table for structured storage and querying.
'create_vector_column': Add a new column to store vector embeddings generated by the Sentence Transformer model.
'install_pgvector_extension': Install the pgvector extension in the PostgreSQL environment to enable native support for vector computations.
'generate_embeddings': Encode restaurant reviews into 384-dimensional vector embeddings and store them in the database.
'execute_cosine_similarity_search': Perform vector similarity queries using the cosine distance metric to identify the most relevant restaurants for user queries.
'save_finalized_table': Save the updated SQL table with all modifications, including the vector embeddings and normalized schema.

**Description**

Following the data cleaning process, the refined dataset was uploaded to a PostgreSQL database to facilitate efficient storage and querying. This step was crucial for enabling advanced vector-based similarity searches in the Michelin Guide Dining Finder.

The dataset was structured into a SQL table, ensuring proper normalization and alignment with relational database best practices. Each column of the table represented key attributes of the cleaned dataset, including the unique identifier, restaurant name, address, description, food type, stars label, ISO country code, and latitude and longitude information. This organization allowed for efficient querying and seamless integration with vector similarity operations.

To enable vector-based computations, we installed the pgvector extension in PostgreSQL. This extension provides native support for storing and querying vector embeddings within the database. By leveraging pgvector, we could store dense vector embeddings directly in the database, enabling efficient similarity searches using cosine distance.

The installation of the pgvector extension was straightforward, requiring the execution of the following command in the PostgreSQL environment:

CREATE EXTENSION IF NOT EXISTS vector;

Once the extension was installed, a new column was added to the SQL table to store the vector embeddings. These embeddings were generated using a pre-trained Sentence Transformer model and represented restaurant reviews in a 384-dimensional vector space. The database schema was updated to accommodate the new column, ensuring compatibility with the vector operations provided by pgvector.

The use of PostgreSQL with the pgvector extension ensured that the Michelin Guide Dining Finder was equipped with a robust and scalable backend, capable of performing complex vector similarity searches efficiently. This setup formed the backbone of our recommendation system, allowing us to deliver personalized restaurant suggestions to users.

The following Entity-Relationship (ER) diagram illustrates the schema design for the Michelin Guide Dining Finder database. It highlights the relationships between the key tables: cleaned_data_with_embeddings and iso_country_codes. The cleaned_data_with_embeddings table stores detailed information about restaurants, including their names, addresses, food types, and vector embeddings for review analysis. The iso_country_codes table provides a reference for standardized country codes, ensuring accurate mapping and consistency across the dataset. This structure enables seamless integration of data for efficient querying and vector-based similarity searches, forming the foundation of the recommendation system.

![Entity-Relationship Diagram](./artifacts/er_diagram.png)


## sentence-transformers ##

**Key Functions:**<br>

`load_csv_data`: Load the input CSV file into a pandas DataFrame for processing.<br>
`add_length_of_lease_column`: Add a new column ‘Length of lease’ and populate it based on the ‘Check Out’ date values.<br>
`drop_unnecessary_columns`: Remove the ‘Cleaning Fee’ and ‘Airbnb Service Fee’ columns from the DataFrame.<br>
`adjust_price_for_one_month`: Modify the ‘Price Per Night’ for rows with a ‘one month’ lease, dividing the price by 30 to reflect the per-night rate.<br>
`save_to_excel`: Save the updated DataFrame to an Excel file.<br>
`adjust_excel_column_widths`: Adjust the widths of specific columns (‘C’ and ‘D’) in the Excel sheet for better readability.<br>
`save_excel_file`: Save the final Excel file after applying all modifications.<br>
`filter_by_lease_length`: Filter the data based on the ‘Length of lease’ column, creating separate DataFrames for ‘one day’, ‘one week’, and ‘one month’ lease durations.<br>

**Description**

This script updates the Length of lease based on Check In and Check Out dates and adjusts prices for records with a length of lease as one week and one month. It also splits the data into three separate files based on the length of lease: one day, one week, and one month. The processed data is saved as Excel files.

**Workflow**

The workflow includes reading the input CSV file, updating the Length of lease based on Check In and Check Out dates, deleting unnecessary columns like Cleaning Fee and Airbnb Service Fee, splitting the data into three files based on the Length of lease, and saving the processed data as Excel files while adjusting the column widths for date columns.

# Visualization And Findings #

## Visualization ##
Using the `python3 code/visualization.py`  on the cmd to run the data. <br>
This part generates a variety of visualizations for analyzing Airbnb prices based on different factors such as city, free parking availability, pet allowance, and smoking policies. It uses Python libraries, including matplotlib, seaborn, and pandas, to create histograms, bar plots, and boxplots from data stored in Excel files .Each of these functions reads data from Excel files, processes it for the respective analysis (e.g., comparing cities, or analyzing policy effects), and generates visualizations, which are saved to a specified output location.

**Key Functions:**

`plot_price_distribution`: Generates a histogram showing one-day Airbnb price distribution.<br>
`plot_city_comparison_boxplot`: Creates a boxplot comparing one-day prices across selected cities.<br>
`plot_pet_combined_price_distributions` Visualizes price distributions for one-day, one-week, and one-month stays based on pet allowance.<br>
`plot_smoking_allowed_boxplots`: Plots boxplots to compare prices for smoking and non-smoking listings.<br>
`plot_free_parking_barplots`: Compares average prices for listings with and without free parking for different lease durations.<br>
'`output_path = "./artifacts/"`: This specifies that the generated visualizations (PNG files) will be saved in a folder named artifacts, which is also located in the current working directory.<br>

##  Findings and Analysis ##
**General Price Distribution**

![](./artifacts/price_distribution.png)
The histogram shows the price distribution of one-day Airbnb listings, with the x-axis representing the price per night and the y-axis showing the frequency of listings at each price point. The distribution is right-skewed, with most one-day Airbnb listings priced between $100–$150. Higher-priced listings above $200 are rare, indicating that the majority of listings are affordable, while luxury options are limited. The skew suggests that more affordable listings dominate the market, with only a few high-end accommodations available.

**City Comparison**

![](./artifacts/city_comparison.png)
The boxplot compares one-day Airbnb prices across four cities: Austin, New York City, Chicago, and Los Angeles. Austin has the highest median price (~$200), while New York City has a broader range with many lower-priced options but also several high-end outliers. Chicago and Los Angeles show more consistent pricing with fewer extreme values. Overall, Austin's prices vary widely, New York City has significant variation, and both Chicago and Los Angeles have more stable pricing with less variation in outliers.

**The effect of free parking**

![Free Parking Effect](./artifacts/combined_barplot_free_parking_price_output.png)
For one-month stays, prices are similar regardless of free parking. For one-day stays, listings with free parking are cheaper. Free parking shows minimal impact on one-week prices but slightly lowers prices for short-term stays. Location could indeed be a key reason for the price differences. In urban areas where parking is scarce, listings without free parking may be in more desirable or central locations, which can drive up their price. Conversely, listings with free parking might be located in less central areas where parking is easier to offer, leading to lower prices for short-term stays. For one-month rentals, location might play less of a role in price differences, as long-term renters may prioritize other factors over parking, such as proximity to work or public transport.

**The effect of pet allowed**

![Pet Policy Effect](./artifacts/combined_price_distributions.png)
The graphs show price distributions for one-month, one-week, and one-day Airbnb listings, separated by whether pets are allowed or not.  In the One-Month Price Distribution (left), listings that allow pets (orange) are generally priced higher than those that do not, especially in the lower price ranges (up to $100). This suggests that pet-friendly long-term rentals may command a premium. In the One-Week Price Distribution (middle), a similar trend is observed, with pet-friendly listings taking a larger share in the higher price ranges compared to non-pet listings, though the difference is less pronounced than for one-month stays. For the One-Day Price Distribution (right), pet-friendly listings are more spread across various price ranges but still maintain a noticeable presence in the lower price brackets. The overall effect of allowing pets is less significant for one-day stays compared to longer-term rentals. Possible reasons for these differences include higher demand for pet-friendly listings, as renters with pets may be willing to pay more for accommodations that meet their needs, especially for long stays. Additionally, added costs for hosts associated with allowing pets, such as maintenance and cleaning, could lead to higher pricing, particularly for longer rental periods.

**The effect of smoking allowed**

![Smoking Policy Effect](./artifacts/combined_boxplot_smoking_allowed_price.png)
The boxplots show price distributions for one-month, one-week, and one-day Airbnb listings, comparing those that allow smoking versus those that do not. Listings that do not allow smoking tend to have higher prices and a wider price range, especially for one-month and one-week stays. This may be due to higher demand for non-smoking accommodations, particularly in family-friendly or urban areas, where smoking is less accepted. Non-smoking listings likely attract a broader market and are perceived as cleaner or more desirable, allowing hosts to charge a premium. Smoking-allowed listings, on the other hand, cater to a more niche audience, which could explain their lower prices and narrower price range, particularly for longer stays. For one-day stays, the price difference is less significant.

# Visualization And Findings #

## Visualization ##
Using the `streamlit run app.py` on the cmd to run the app.


## Interactive Map with Nearest Restaurants

**Key Functions:** <br>
`interactive_map`: Main function to display an interactive map with Michelin restaurants and compute nearest restaurant information.
`query_data`: Utilize PostgreSQL's GIS capabilities to query restaurant data and convert it into a GeoDataFrame for spatial analysis.
`get_nearest_restaurants`: Calculate the nearest restaurants to a user-selected point on the map using geometric distance computations.

**Processing Logic:**<br>
The `interactive_map` function takes advantage of PostgreSQL's GIS capabilities to extract restaurant details, including geographic coordinates, via the `query_data` function. This data is converted into a GeoDataFrame, leveraging its geometry support for spatial computations. An interactive map is generated using Folium, where each restaurant is represented as a marker. When a user clicks on a point on the map, `get_nearest_restaurants` computes the 10 closest restaurants using spatial distance calculations provided by the GeoDataFrame's geometry. The results are displayed in a sorted table by star rating, providing users with an intuitive and interactive experience.

![image](https://github.com/yishanyuan/Final_Project_2024/blob/main/artifacts/interactive_map.png) <br>
![image](https://github.com/yishanyuan/Final_Project_2024/blob/main/artifacts/interactive_map_result.png)

<br>

# Limitation

1. Vector Search Limitations:<br>
The current vector search relies on 384-dimensional embeddings generated by Sentence Transformers and PGVector. This dimensionality may result in better performance for multi-word queries compared to single-word queries, limiting the consistency of results across varying query lengths.<br>
2. Limited Full-Text Search Data:<br>
The dataset used for full-text search is relatively small, which restricts the diversity and richness of search results.

<br>

#  Further Research
1. Enhancing the Machine Learning Model:<br>
Experiment with machine learning models that support higher-dimensional vector representations to capture more intricate relationships and subtle nuances in the data. Incorporate advanced pre-trained language models (e.g., BERT or GPT-based embeddings) to enhance the quality and relevance of AI-powered search results.<br>
2. Expanding the Dataset:<br>
Integrate Google Reviews into the dataset to provide more context and enrich the information available for search and machine learning functionalities. Include data from other restaurant ranking systems or user-generated platforms, creating a more comprehensive and versatile dataset.<br>
3. Real-Time Data Updates:<br>
Develop automated ETL (Extract, Transform, Load) pipelines to regularly update Michelin data. This ensures the application always reflects the most current and accurate restaurant information.<br>
4. Geographic Expansion:<br>
Extend the dataset to include restaurants from regions not covered by the Michelin Guide, leveraging alternative restaurant evaluation platforms or open data sources to broaden geographic coverage.<br>
<br>








