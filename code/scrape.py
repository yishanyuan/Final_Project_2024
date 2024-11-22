import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_res import scrape_res


def scrape():
    """Scrape everything and return a list of books."""
    res_urls = scrape_all_pages()
    res = scrape_res(res_urls)
    return res

def write_res_to_csv(reses, path):
    with open (path, "w", newline = "") as file:
        write = csv.DictWriter(file, reses[0].keys())
        write.writeheader()
        write.writerows(reses)
    return

def write_res_to_json(reses, path):
    with open (path, "w", newline = "", encoding = "utf-8") as file:
        for res in reses:
            json.dump(res, file)
            file.write("\n")
        
    pass

if __name__ == "__main__":

    BASE_DIR = "data"
    CSV_PATH = os.path.join(BASE_DIR, "raw_results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "raw_results.json")
    os.makedirs(BASE_DIR, exist_ok=True)

    reses = scrape()

    write_res_to_csv(reses, CSV_PATH)
    write_res_to_json(reses, JSONL_PATH)
