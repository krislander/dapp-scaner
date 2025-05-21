import requests
from data_fetcher.utils import get_api_key

def fetch_dappradar(limit=100):
    """
    Fetch top-*limit* DApps from DappRadar API.
    Requires API key in config/config.ini under [dappradar].
    """
    api_key = get_api_key("dappradar")
    headers = {"x-api-key": api_key}
    params  = {"limit": limit}
    resp    = requests.get("https://api.dappradar.com/v1/dapps",
                           headers=headers, params=params)
    items   = resp.json().get("data", [])
    return [
        {
            "source":   "dappradar",
            "name":     i["name"],
            "slug":     i["slug"],
            "category": i.get("category", ""),
            "tvl":      i.get("tvl", 0),
            "users":    i.get("activeUsers", 0)
        }
        for i in items
    ]
