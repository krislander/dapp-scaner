import requests
from configparser import ConfigParser
import os

# load API key
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
API_KEY = _cfg["dappradar"]["api_key"]
API_ORIGIN = _cfg["dappradar"]["api_origin"]

def fetch_dappradar(limit=100):
    """
    Fetch top-*limit* DApps from DappRadar API and
    normalize to our schema:
      {
        "name": str,
        "slug": str,
        "category": str,
        "chains": [str],
        "metrics": {"tvl": float, "users": int}
      }
    """
    headers = {"x-api-key": API_KEY}
    params  = {"limit": limit}
    resp    = requests.get(API_ORIGIN + "dapps",
                           headers=headers, params=params)
    resp.raise_for_status()
    items = resp.json().get("data", [])

    records = []
    for i in items:
        records.append({
            "name":     i["name"],
            "slug":     i["slug"],
            "category": i.get("category", "") or "",
            "chains":   i.get("blockchains", []),
            "metrics": {
                "tvl":   float(i.get("tvl", 0)),
                "users": int(i.get("activeUsers", 0)),
            }
        })
    return records
