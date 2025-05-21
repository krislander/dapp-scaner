import requests

def fetch_defillama(limit=100):
    """
    Fetch top-*limit* protocols by TVL from DeFiLlama API.
    """
    resp = requests.get("https://api.llama.fi/protocols")
    data = resp.json()
    # sort descending by tvl
    sorted_data = sorted(data, key=lambda x: x.get("tvl", 0), reverse=True)
    top = sorted_data[:limit]
    return [
        {
            "source":   "defillama",
            "name":     d["name"],
            "slug":     d["slug"],
            "category": d.get("category", ""),
            "tvl":      d.get("tvl", 0),
            "users":    d.get("users", 0)
        }
        for d in top
    ]
