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

## Extract Check-in and Check-out Dates from URLs
Using regular expressions to extract the check_in and check_out dates from each listing's URL and adds these dates to the listing details.

**Regular Expression Pattern:** The pattern `r'check_in=(\d{4}-\d{2}-\d{2})&check_out=(\d{4}-\d{2}-\d{2})'` matches URLs containing dates such as check_in=2024-11-01&check_out=2024-11-05.
If a match is found, the two dates (check_in and check_out) are captured.

**Processing Logic:** Iterate through all the listings, checking each URL for a match.
If the dates are found, add them to the corresponding listing details.
Store the updated listings in a new dictionary for further processing.


## Assign Cities Based on Check-out Dates
Assigning cities to each listing based on specific check-out dates. When certain dates are encountered, the city is switched to the next one in the predefined list.

**Key dates:** When the check_out date is `"2024-11-30"`, it signals the start of a new batch.
If `"2024-11-02"` is encountered after this batch starts, the city assignment will rotate to the next city.

**City List:** The predefined city list is: `["Austin, TX", "New York City, NY", "Chicago, IL", "Los Angeles, CA"].`
The logic rotates through the list using city indexes, updating the assigned city whenever the key dates trigger a rotation.

**Processing Logic:** Initialize the city index to 0 (pointing to the first city, Austin, TX).
Iterate through the listings:
If the check_out date is `"2024-11-30"`, mark it as a new batch.
If `"2024-11-02"` is found within the new batch, advance the city index to the next city.
Assign the city corresponding to the current index to each listing.


## Remove Invalid Records
The valid data is retained by applying several filtering conditions:

**Filtering Conditions:** The URL must start with `https`. Otherwise, the listing is removed.
features, prices, and house_rules must all contain valid data. If any of these fields are empty, the listing is discarded.

**Processing Logic:** Iterate through the listings, checking if each URL starts with https.
Use the `len()` function to ensure that features, prices, and house_rules are not empty.
If a listing meets all the criteria, it is added to the cleaned data dictionary.

## Load and Save JSON Data
The program includes functions to load data from a JSON file and save the processed data into a new JSON file.


# Manipulate Data
Using the `python3 code/Change_file_format.py`, `python3 code/manipulated_variables.py`, `python3 code/sort_into_different_time_files.py` and `python3 code/split_data.py` on the cmd to run the data.

## JSON to CSV Conversion ##

**Key Functions:**<br>

`load_json_data`: Load the JSON data from a specified file path.<br>
`write_csv_header`: Write the header to the output CSV file.<br>
`write_csv_rows`: Write rows of room data extracted from the JSON file into the CSV.<br>
get_row_details: Extract specific room details (city, check-in/check-out, features, and pricing information) for each property from the JSON data.<br>
`generate_csv`: Create a CSV file with the extracted room data including URL, features, and pricing details.<br>
`close_json_file`: Close the JSON file after reading all the data.<br>

**Processing Logic:**

This script converts processed JSON files (e.g., cleaned_data.json) into CSV files. It reads data from a JSON file, extracts fields such as URL, city, check-in/check-out dates, features, and price details, and writes the data into CSV format. The generated CSV file is saved in the data folder. The workflow involves reading JSON data from cleaned_data.json, extracting fields like city, check-in/check-out dates, features, and prices, converting the data into CSV format, and saving the output CSV file (e.g., output_data.csv) to the data folder.

## CSV Enhancement ##

**Key Functions:**<br>

`load_csv_data`: Load the input CSV file into a pandas DataFrame for further processing.<br>
`define_base_directory`: Define the base directory for the project by moving up one level from the current file location.<br>
`extract_and_add_feature_columns`: Add new feature columns (e.g., ‘Smoking allowed’, ‘Pets allowed’, ‘Free parking’) by checking if specific keywords are present in the ‘Features’ column.<br>
`save_updated_csv`: Save the modified DataFrame (with additional feature columns) to a new CSV file.<br>
`close_csv_file`: Close the original CSV file once the data is read and processed.<br>


**Description**

This script updates an existing CSV file by adding new columns such as Smoking allowed, Pets allowed, and Free parking. It also adds a Length of lease column based on the check-out date, marking rows as one day, one week, or one month.

**Workflow**

The workflow includes reading the input CSV file (e.g., path_to_your_existing_csv_file.csv) from the data folder, scanning the Features column to check for Smoking allowed, Pets allowed, and Free parking, adding corresponding columns to indicate whether these features are available, adding a Length of lease column based on specific check-out dates, and saving the updated CSV file to the data folder.

## Data Processing and Price Adjustment ##

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








