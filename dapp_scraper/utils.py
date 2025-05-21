import os
import configparser
import requests
from bs4 import BeautifulSoup

# load config.ini
CFG = configparser.ConfigParser()
cfg_path = os.path.join(os.path.dirname(__file__), os.pardir, "config", "config.ini")
CFG.read(cfg_path)

def get_database_url():
    return CFG["database"]["url"]

def get_api_key(service_name):
    return CFG[service_name]["api_key"]

def fetch_deepdao(limit=100):
    """
    Fallback scraper for DeepDAO homepage.
    Returns list of dicts like other fetchers.
    """
    url  = "https://deepdao.io/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table tr")[1:limit+1]  # skip header
    out = []
    for tr in rows:
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        # expected cols: [rank, name, tvl, members, ...]
        name        = cols[1]
        tvl_str     = cols[2]
        users_str   = cols[3]
        tvl         = float(tvl_str.replace("$","").replace(",",""))
        users       = int(users_str.replace(",",""))
        out.append({
            "source":   "deepdao",
            "name":     name,
            "slug":     name.lower().replace(" ", "-"),
            "category": "",
            "tvl":      tvl,
            "users":    users
        })
    return out
