import requests
from configparser import ConfigParser
import os

from scripts import rate_limiter

# load API key
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
API_KEY = _cfg["dappradar"]["api_key"]
API_ORIGIN = _cfg["dappradar"]["api_origin"]

rate_limiter = rate_limiter.DappRadarRateLimiter()

def make_rate_limited_request(url, headers, params=None):
    """
    Make a rate-limited request to DappRadar API
    """
    rate_limiter.wait_if_needed()
    return requests.get(url, headers=headers, params=params)

def fetch_dappradar(limit):
    """
    Fetch top DApps from DappRadar API by categories
    Makes exactly 9 requests (one per category) and returns normalized data
    """
    headers = {"x-api-key": API_KEY}
    categories = ['games', 'defi', 'collectibles', 'marketplaces', 'high-risk', 'gambling', 'exchanges', 'social', 'other']
    
    print(f"🚀 Fetching DApps from {len(categories)} categories...")
    
    try:        
        all_records = []
        
        # Iterate through each category (exactly 9 requests)
        for category in categories:
            print(f"📱 Fetching category: {category}")
            
            params = {
                "category": category,
                "top": limit
            }
            
            try:
                resp = make_rate_limited_request(API_ORIGIN + "dapps/top/uaw", headers, params)
                
                if resp.status_code != 200:
                    raise Exception(f"DappRadar API request failed for category '{category}' with status code {resp.status_code}. Response: {resp.text[:200]}")
                
                items = resp.json().get("results", [])
                
                if not items:
                    print(f"⚠️ No data for {category}")
                    continue
                
                print(f"✅ {category}: {len(items)} DApps")
                
                # Process each DApp for this category
                for result in items:
                    # DApp data is directly in the result object
                    if not result:
                        continue
                    
                    # Extract chains - they are directly an array of strings
                    chains = result.get("chains", [])
                    
                    # Extract categories - they are directly an array of strings
                    categories_list = result.get("categories", [])
                    
                    # Get metrics
                    metrics = result.get("metrics", {})
                    
                    # Generate slug from name if not available
                    dapp_name = result.get("name", "")
                    dapp_slug = dapp_name.lower().replace(" ", "-").replace(".", "") if dapp_name else ""
                    
                    # Helper function to safely convert to int/float
                    def safe_int(value, default=0):
                        try:
                            return int(value) if value is not None else default
                        except (ValueError, TypeError):
                            return default
                    
                    def safe_float(value, default=0.0):
                        try:
                            return float(value) if value is not None else default
                        except (ValueError, TypeError):
                            return default
                    
                    record = {
                        "name": dapp_name,
                        "slug": dapp_slug,
                        "category": categories_list[0] if categories_list else category,
                        "chains": chains,
                        "status": "active",
                        "multi_chain": len(chains) > 1,
                        "birth_date": None,
                        "ownership_status": None,
                        "capital_raised": 0,
                        "showcase_fun": False,
                        "decentralisation_lvl": None,
                        "industry": categories_list[0] if categories_list else "",
                        "source_chain": chains[0] if chains else "",
                        "metrics": {
                            "tvl": 0,  # Not available in this endpoint
                            "users": safe_int(metrics.get("uaw")),
                            "volume": safe_float(metrics.get("volume")),
                            "transactions": safe_int(metrics.get("transactions")),
                            "balance": safe_float(metrics.get("balance")),
                        },
                        "tokens": [],
                        "protocols": [],
                        "fees": [],
                        "governance": [],
                        "activities": [],
                        "funding": []
                    }
                    
                    all_records.append(record)
                
            except Exception as chain_error:
                print(f"❌ Error fetching {category}: {chain_error}")
            
        
        if not all_records:
            print("⚠️ No data retrieved from DappRadar")
            return []
        
        # Remove duplicates based on slug
        unique_records = {}
        for record in all_records:
            slug = record.get('slug')
            if slug and slug not in unique_records:
                unique_records[slug] = record
            elif slug:
                # If duplicate, merge chain information
                existing_chains = set(unique_records[slug].get('chains', []))
                new_chains = set(record.get('chains', []))
                merged_chains = list(existing_chains.union(new_chains))
                unique_records[slug]['chains'] = merged_chains
                unique_records[slug]['multi_chain'] = len(merged_chains) > 1
                
                # Keep the record with higher metrics
                if record.get('metrics', {}).get('tvl', 0) > unique_records[slug].get('metrics', {}).get('tvl', 0):
                    unique_records[slug] = record
                    unique_records[slug]['chains'] = merged_chains
                    unique_records[slug]['multi_chain'] = len(merged_chains) > 1
        
        final_records = list(unique_records.values())
        print(f"🎉 Collected {len(final_records)} unique DApps from {len(categories)} categories")
        
        return final_records

    except Exception as e:
        print(f"❌ DappRadar API error: {e}")
        return []


