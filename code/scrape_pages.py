
from common import get_soup
URL = "https://guide.michelin.com/us/en/restaurants/all-starred/bib-gourmand/page/"


def scrape_page(num):
    """Takes a page and returns a list of links to the restaurant that are on the page."""
    url = URL + str(num)
    res_links = get_soup(url).find_all("h3", class_ = "card__menu-content--title pl-text pl-big js-match-height-title")
    links = []
    for res in res_links:
        for a_tag in res.find_all("a", href = True):
            href = a_tag.get("href")
            full_link = "https://guide.michelin.com/" + str(href)
            links.append(full_link)

    return links

def scrape_all_pages():
    """Scrapes all pages, returning a list of reatsaurant links."""
    page = 1

    links = []

    while True:

        page_data = scrape_page(page)

        if not page_data:
            break

        page += 1
        links += page_data

    return links
    

