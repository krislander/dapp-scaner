import requests

def fetch_defillama(limit=100):
    """
    Fetch top-*limit* protocols by TVL from DeFiLlama API and
    normalize to our schema:
      {
        "name": str,
        "slug": str,
        "category": str,
        "chains": [str],
        "metrics": {"tvl": float, "users": int}
      }
    """
    resp = requests.get("https://api.llama.fi/protocols")
    resp.raise_for_status()
    data = resp.json()
    # sort by TVL desc and take top-N
    top = sorted(data, key=lambda x: x.get("tvl", 0), reverse=True)[:limit]

    records = []
    for item in top:
        records.append({
            "name":     item["name"],
            "slug":     item["slug"],
            "category": item.get("category", "") or "",
            "chains":   item.get("chains", []),
            "metrics": {
                "tvl":   float(item.get("tvl", 0)),
                "users": int(item.get("users", 0)),
            }
        })
    return records
