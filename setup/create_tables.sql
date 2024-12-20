-- Optional Step: Drop tables if they exist 
DROP TABLE IF EXISTS cleaned_data CASCADE;
DROP TABLE IF EXISTS iso_country_codes CASCADE;

-- Create the ISO Country Codes Table
CREATE TABLE iso_country_codes (
    iso_code CHAR(10) PRIMARY KEY, 
    country VARCHAR(255) NOT NULL 
);

-- Create an index for faster querying of the country column
CREATE INDEX iso_country_idx ON iso_country_codes (country);

-- Create the Cleaned Data Table
CREATE TABLE cleaned_data (
    UniqueID VARCHAR(255) PRIMARY KEY, 
    name VARCHAR(255) NOT NULL, 
    address TEXT, 
    description TEXT, 
    facilities_services TEXT, 
    latitude_and_longitude TEXT, 
    food_type VARCHAR(100), 
    country VARCHAR(100), 
    stars_label VARCHAR(255), 
    ISO_Code CHAR(10), 
    CONSTRAINT fk_iso_code FOREIGN KEY (ISO_Code) REFERENCES iso_country_codes(iso_code) 
);

-- Create indexes in the cleaned_data table
CREATE INDEX name_idx ON cleaned_data (name);
CREATE INDEX food_type_idx ON cleaned_data (food_type);
CREATE INDEX country_idx ON cleaned_data (country);
CREATE INDEX stars_label_idx ON cleaned_data (stars_label);

