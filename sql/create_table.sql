-- To install the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Optional Step: Drop tables if they exist 
DROP TABLE IF EXISTS cleaned_data_with_embeddings CASCADE;
DROP TABLE IF EXISTS iso_country_codes CASCADE;

-- Create the ISO Country Codes Table
CREATE TABLE iso_country_codes (
    iso_code CHAR(10) PRIMARY KEY, 
    country VARCHAR(255) NOT NULL 
);

-- Create an index for faster querying of the country column
CREATE INDEX iso_country_idx ON iso_country_codes (country);

-- Create the Cleaned Data Table
CREATE TABLE cleaned_data_with_embeddings (
    UniqueID VARCHAR(255) PRIMARY KEY, 
    name VARCHAR(255) NOCREATE EXTENSION IF NOT EXISTS vector;

-- Optional Step: Drop tables if they exist 
DROP TABLE IF EXISTS cleaned_data_with_embeddings CASCADE;
DROP TABLE IF EXISTS iso_country_codes CASCADE;

-- Create the ISO Country Codes Table
CREATE TABLE iso_country_codes (
    iso_code CHAR(10) PRIMARY KEY, 
    country VARCHAR(255) NOT NULL 
);

-- Create an index for faster querying of the country column
CREATE INDEX iso_country_idx ON iso_country_codes (country);

-- Create the Cleaned Data Table
CREATE TABLE cleaned_data_with_embeddings (
    UniqueID VARCHAR(255) PRIMARY KEY, 
    name VARCHAR(255) NOT NULL, 
    address TEXT, 
    description TEXT, 
    facilities_services TEXT, 
    latitude_and_longitude TEXT, 
    food_type VARCHAR(100), 
    country VARCHAR(100), 
    stars_label VARCHAR(255), 
    price_symbol_count VARCHAR(255),
    ISO_Code CHAR(10), 
    embedding vector(384)
    );

-- Create indexes in the cleaned_data table
CREATE INDEX name_idx ON cleaned_data_with_embeddings (name);
CREATE INDEX food_type_idx ON cleaned_data_with_embeddings (food_type);
CREATE INDEX country_idx ON cleaned_data_with_embeddings (country);
CREATE INDEX stars_label_idx ON cleaned_data_with_embeddings (stars_label);T NULL, 
    address TEXT, 
    description TEXT, 
    facilities_services TEXT, 
    latitude_and_longitude TEXT, 
    food_type VARCHAR(100), 
    country VARCHAR(100), 
    stars_label VARCHAR(255), 
    price_symbol_count VARCHAR(255),
    ISO_Code CHAR(10), 
    embedding vector(384)
    );

-- Create indexes in the cleaned_data table
CREATE INDEX name_idx ON cleaned_data_with_embeddings (name);
CREATE INDEX food_type_idx ON cleaned_data_with_embeddings (food_type);
CREATE INDEX country_idx ON cleaned_data_with_embeddings (country);
CREATE INDEX stars_label_idx ON cleaned_data_with_embeddings (stars_label);



