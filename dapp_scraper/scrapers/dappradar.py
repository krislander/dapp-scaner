import requests
from configparser import ConfigParser
import os
from datetime import datetime
import time

# load API key
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
API_KEY = _cfg["dappradar"]["api_key"]
API_ORIGIN = _cfg["dappradar"]["api_origin"]

def fetch_dappradar(limit=100):
    """
    Fetch top-*limit* DApps from DappRadar API and
    normalize to our schema with comprehensive data
    """
    headers = {"x-api-key": API_KEY}
    
    # Get basic DApp list
    params = {"limit": limit}
    
    try:
        print(f"Making request to: {API_ORIGIN}dapps")
        print(f"Headers: x-api-key: {API_KEY[:10]}...")
        print(f"Params: {params}")
        
        resp = requests.get(API_ORIGIN + "dapps", headers=headers, params=params)
        
        print(f"Response status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Response text: {resp.text[:500]}...")
            print("❌ DappRadar API returned error - using fallback data")
            return get_sample_dappradar_data(limit)
        
        resp.raise_for_status()
        items = resp.json().get("data", [])
        
        if not items:
            print("⚠️ No data returned from DappRadar API - using fallback data")
            return get_sample_dappradar_data(limit)

    except Exception as e:
        print(f"❌ DappRadar API error: {e}")
        print("🔄 Using fallback sample data instead")
        return get_sample_dappradar_data(limit)

    records = []
    for i, dapp in enumerate(items):
        print(f"Processing DApp {i+1}/{len(items)}: {dapp['name']}")
        
        # Get detailed information for each DApp
        detailed_data = get_dapp_details(dapp.get('id'), headers)
        
        record = {
            "name": dapp["name"],
            "slug": dapp["slug"],
            "category": dapp.get("category", "") or "",
            "chains": dapp.get("blockchains", []),
            "status": "active",  # Default status
            "multi_chain": len(dapp.get("blockchains", [])) > 1,
            "birth_date": None,
            "ownership_status": None,
            "capital_raised": 0,
            "showcase_fun": False,
            "decentralisation_lvl": None,
            "industry": dapp.get("industry", ""),
            "metrics": {
                "tvl": float(dapp.get("tvl", 0)),
                "users": int(dapp.get("activeUsers", 0)),
                "volume": float(dapp.get("volume", 0)),
                "transactions": int(dapp.get("transactions", 0)),
                "balance": float(dapp.get("balance", 0)),
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": [],
            "funding": []
        }
        
        # Merge detailed data if available
        if detailed_data:
            record.update(detailed_data)
        
        records.append(record)
        
        # Rate limiting to avoid API limits
        time.sleep(0.1)

    return records

def get_sample_dappradar_data(limit=10):
    """
    Fallback sample data when DappRadar API fails
    """
    sample_data = [
        {
            "name": "PancakeSwap",
            "slug": "pancakeswap",
            "category": "DeFi",
            "industry": "DeFi",
            "chains": ["BSC"],
            "status": "active",
            "multi_chain": False,
            "birth_date": datetime(2020, 9, 1).date(),
            "ownership_status": "Decentralized",
            "capital_raised": 0,
            "showcase_fun": True,
            "decentralisation_lvl": "high",
            "metrics": {
                "tvl": 2100000000,
                "users": 18000,
                "volume": 850000000,
                "transactions": 1200000,
                "balance": 2100000000,
            },
            "tokens": [{
                "name": "PancakeSwap",
                "symbol": "CAKE",
                "format": "BEP-20"
            }],
            "protocols": [],
            "fees": [{
                "type": "Trading Fee",
                "rate": 0.0025,
                "charged_to": "Traders",
                "recipient": "Liquidity Providers"
            }],
            "governance": ["DAO"],
            "activities": ["DEX", "Yield Farming"],
            "funding": []
        },
        {
            "name": "OpenSea",
            "slug": "opensea",
            "category": "Marketplaces",
            "industry": "NFT",
            "chains": ["Ethereum", "Polygon"],
            "status": "active",
            "multi_chain": True,
            "birth_date": datetime(2017, 12, 1).date(),
            "ownership_status": "Centralized",
            "capital_raised": 300000000,
            "showcase_fun": True,
            "decentralisation_lvl": "low",
            "metrics": {
                "tvl": 0,
                "users": 45000,
                "volume": 2800000000,
                "transactions": 850000,
                "balance": 0,
            },
            "tokens": [],
            "protocols": [],
            "fees": [{
                "type": "Marketplace Fee",
                "rate": 0.025,
                "charged_to": "Sellers",
                "recipient": "Platform"
            }],
            "governance": [],
            "activities": ["NFT Trading", "Marketplace"],
            "funding": [{
                "source": "Venture Capital",
                "amount": 300000000
            }]
        },
        {
            "name": "MetaMask",
            "slug": "metamask",
            "category": "Wallets",
            "industry": "Infrastructure",
            "chains": ["Ethereum", "BSC", "Polygon"],
            "status": "active",
            "multi_chain": True,
            "birth_date": datetime(2016, 7, 1).date(),
            "ownership_status": "Centralized",
            "capital_raised": 0,
            "showcase_fun": False,
            "decentralisation_lvl": "medium",
            "metrics": {
                "tvl": 0,
                "users": 100000000,
                "volume": 0,
                "transactions": 0,
                "balance": 0,
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": ["Wallet", "Browser Extension"],
            "funding": []
        }
    ]
    
    return sample_data[:limit]

def get_dapp_details(dapp_id, headers):
    """
    Get detailed information for a specific DApp
    """
    try:
        # Get DApp details
        detail_resp = requests.get(f"{API_ORIGIN}dapps/{dapp_id}", headers=headers)
        if detail_resp.status_code == 200:
            detail_data = detail_resp.json().get("data", {})
            
            details = {}
            
            # Extract launch date if available
            if detail_data.get("launchDate"):
                try:
                    details["birth_date"] = datetime.fromisoformat(detail_data["launchDate"].replace('Z', '+00:00')).date()
                except:
                    pass
            
            # Extract description and categorize
            description = detail_data.get("description", "")
            if description:
                details["description"] = description
                # Simple heuristics to determine decentralization level
                if any(word in description.lower() for word in ["decentralized", "dao", "governance"]):
                    details["decentralisation_lvl"] = "high"
                elif any(word in description.lower() for word in ["centralized", "company", "team"]):
                    details["decentralisation_lvl"] = "low"
                else:
                    details["decentralisation_lvl"] = "medium"
            
            # Extract website and social links
            if detail_data.get("website"):
                details["website"] = detail_data["website"]
            
            # Extract token information if available
            tokens = []
            if detail_data.get("token"):
                token_info = detail_data["token"]
                tokens.append({
                    "name": token_info.get("name", ""),
                    "symbol": token_info.get("symbol", ""),
                    "format": token_info.get("standard", "ERC-20")  # Default to ERC-20
                })
            details["tokens"] = tokens
            
            # Extract additional metrics
            additional_metrics = {}
            if detail_data.get("dappRankings"):
                rankings = detail_data["dappRankings"]
                additional_metrics.update({
                    "ranking_overall": rankings.get("overall", 0),
                    "ranking_category": rankings.get("category", 0),
                })
            
            # Social metrics
            if detail_data.get("socialStats"):
                social = detail_data["socialStats"]
                additional_metrics.update({
                    "twitter_followers": social.get("twitterFollowers", 0),
                    "discord_members": social.get("discordMembers", 0),
                    "telegram_members": social.get("telegramMembers", 0),
                })
            
            if additional_metrics:
                if "metrics" not in details:
                    details["metrics"] = {}
                details["metrics"].update(additional_metrics)
            
            return details
            
    except Exception as e:
        print(f"Error fetching details for DApp {dapp_id}: {e}")
        return {}
    
    return {}

def get_dapp_history(dapp_id, headers, days=30):
    """
    Get historical data for a DApp
    """
    try:
        params = {"range": f"{days}d"}
        hist_resp = requests.get(f"{API_ORIGIN}dapps/{dapp_id}/history", headers=headers, params=params)
        if hist_resp.status_code == 200:
            return hist_resp.json().get("data", [])
    except Exception as e:
        print(f"Error fetching history for DApp {dapp_id}: {e}")
    return []
