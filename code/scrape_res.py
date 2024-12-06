from common import get_soup
import googlemaps
import requests
import os
import sys
import dotenv
dotenv.load_dotenv(".env")
GOOGLE_PLACE_API_KEY = os.environ["GOOGLE_PLACE_API_KEY"]
map_client = googlemaps.Client(GOOGLE_PLACE_API_KEY)

def get_name(soup):
    """ Extracts the title from the BeautifulSoup instance representing a restaurant page as a string."""
    res_name = soup.find("div", class_ = "col col-12 col-lg-12")
    h1_tag = res_name.find("h1")
    title = h1_tag.getText()
    
    return title

def get_address(soup):
    res_address = soup.find_all("div", class_="data-sheet__block--text")[0].getText().strip()
    return res_address

def get_country(soup):
    res_country = soup.find_all("div", class_="data-sheet__block--text")[0].getText().split(",")[-1].strip()
    return res_country



def get_price(soup):
    res_price = soup.find_all("div", class_ = "data-sheet__block--text")[1].getText().split()[0].strip()
    return res_price

def get_type_food(soup):
    res_type = soup.find_all("div", class_ = "data-sheet__block--text")[1].getText().split("·")[1].strip()
    return res_type


def get_stars(soup):
    res_stars = soup.find_all("div", class_ = ("section section-main"))[0]
    res_stars_rows = res_stars.find_all("div", class_ = "row")
    if len(res_stars_rows) > 1:
        distinction_info = res_stars_rows[0].find_all("div", class_ = "data-sheet__classification-item--content")
        if len(distinction_info) > 0:
            distinction = distinction_info[1].getText().strip()
            return distinction
        else:
            return "Selected Restaurants"      
    else:
        return "Selected Restaurants"


def get_description(soup):
    description = soup.find_all("div", class_ = "data-sheet__description")[0].getText().strip()
    return description


def get_facilities_services_info(soup):
    res_facil_serv_info = soup.find_all("div", class_ = "modal modal__common fade")[0]
    facil_serv_info = res_facil_serv_info.find_all("li")
    facil_serv_list = []
    for i in range(len(facil_serv_info)):
        li_text = str(facil_serv_info[i].getText().strip())
        facil_serv_list.append(li_text)
    
    return facil_serv_list

def get_res_lat_long(soup):
    name = get_name(soup)
    country = get_country(soup)
    query_request = f"{name}, {country}"
    response = map_client.places(query = query_request)
    results = response.get("results")
    if len(results) > 0:
        lat_long = results[0]["geometry"]["location"]
    else:
        lat_long = "N/A"
    return lat_long


def scrape_res_dict(res_url):
    soup = get_soup(res_url)
    #dict_info = get_res_information(soup)
    scraped_res_dict = {
        "name": get_name(soup),
        "address": get_address(soup),
        "price": get_price(soup),
        "stars": get_stars(soup),
        "description": get_description(soup),
        "facilities_services": get_facilities_services_info(soup),
        #"rating": dict_info["rating"],
        "latitude and longitude": get_res_lat_long(soup),
        #"numbers of users' reviews": dict_info["numbers of reviews"]
        "food type": get_type_food(soup)
    }
    return scraped_res_dict

def scrape_res(res_urls):
    scrape_res_info = []
    for res_url in res_urls:
        scraped_res = scrape_res_dict(res_url)
        scrape_res_info.append(scraped_res)
        
    return scrape_res_info


