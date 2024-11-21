from common import get_soup

def get_name(soup):
    """ Extracts the title from the BeautifulSoup instance representing a restaurant page as a string."""
    res_name = soup.find("div", class_ = "col col-12 col-lg-12")
    h1_tag = res_name.find("h1")
    title = h1_tag.getText()
    print(title)
    
    return title

def get_address(soup):
    res_address = soup.find_all("div", class_="data-sheet__block--text")[0].getText().strip()
    return res_address

def get_price(soup):
    res_price = soup.find_all("div", class_ = "data-sheet__block--text")[1].getText().split()[0].strip()
    return res_price

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
    res_facil_serv_info = soup.find_all("section", class_ = "section section-main")[0]
    facil_serv_info = res_facil_serv_info.find_all("li")
    facil_serv_list = []
    for i in range(len(facil_serv_info)):
        li_text = str(facil_serv_info[i].getText().strip())
        facil_serv_list.append(li_text)
    
    return facil_serv_list

"""
def get_latitude_longitude(soup):
    res_lat_lon = soup.find_all("section", class_ = "section section-main")[1]
    lat_lon = res_lat_lon.find_all("div", class_ = "place-name")
    return lat_lon

print(get_latitude_longitude(get_soup("https://guide.michelin.com/en/pulau-pinang/my-george-town/restaurant/lum-lai-duck-meat-koay-teow-th-ng")))
print(get_latitude_longitude(get_soup("https://guide.michelin.com/en/kuala-lumpur-region/kuala-lumpur/restaurant/leen-s")))
print(get_latitude_longitude(get_soup("https://guide.michelin.com/en/kuala-lumpur-region/kuala-lumpur/restaurant/frangipaani")))
"""

def scrape_res_dict(res_url):
    soup = get_soup(res_url)
    scraped_res_dict = {
        "name": get_name(soup),
        "address": get_address(soup),
        "price": get_price(soup),
        "stars": get_stars(soup),
        "description": get_description(soup),
        "facilities_services": get_facilities_services_info(soup)
    }
    
    return scraped_res_dict

def scrape_res(res_urls):
    scrape_res_info = []
    for res_url in res_urls:
        scraped_res = scrape_res_dict(res_url)
        scrape_res_info.append(scraped_res)
        
    return scrape_res_info

