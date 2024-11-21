import requests
from bs4 import BeautifulSoup
import os
import csv

url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    div_col = soup.find('div', class_='div-col', style='column-width: 20em;')
    
    if div_col:
        list_items = div_col.find_all('li')
        
        iso_country_data = []
        for item in list_items:
            iso_code_span = item.find('span', class_='monospaced')
            if iso_code_span:
                iso_code = iso_code_span.text.strip()
                country_name_tag = item.find('a')
                if country_name_tag:
                    country_name = country_name_tag.text.strip()
                    iso_country_data.append({'ISO Code': iso_code, 'Country': country_name})  

output_dir = "artifacts"
output_path = os.path.join(output_dir, "iso_country_codes.csv")


with open(output_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ISO Code', 'Country'])
    writer.writeheader()
    writer.writerows(iso_country_data)
