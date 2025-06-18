import requests
from datetime import datetime
import time

def fetch_defillama(limit):
    """
    Fetch top-*limit* protocols by TVL from DeFiLlama API and
    normalize to our schema with comprehensive data
    """
    # Get basic protocols list
    resp = requests.get("https://api.llama.fi/protocols")
    resp.raise_for_status()
    data = resp.json()
    
    # Sort by TVL desc and take top-N (handle None values)
    def safe_tvl(protocol):
        tvl = protocol.get("tvl")
        return tvl if tvl is not None else 0
    
    top = sorted(data, key=safe_tvl, reverse=True)[:limit]

    records = []
    for i, protocol in enumerate(top):
        print(f"Processing Protocol {i+1}/{len(top)}: {protocol['name']}")
        
        # Get detailed information for each protocol
        detailed_data = get_protocol_details(protocol['slug'])
        
        # Safe value extraction with None handling
        def safe_float(value):
            if value is None:
                return 0.0
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        def safe_int(value):
            if value is None:
                return 0
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        
        record = {
            "name": protocol["name"],
            "slug": protocol["slug"],
            "category": protocol.get("category", "") or "",
            "chains": protocol.get("chains", []),
            "status": "active",
            "multi_chain": len(protocol.get("chains", [])) > 1,
            "birth_date": None,
            "ownership_status": None,
            "capital_raised": 0,
            "showcase_fun": False,
            "decentralisation_lvl": None,
            "industry": "DeFi",  # Default for DeFiLlama
            "metrics": {
                "tvl": safe_float(protocol.get("tvl")),
                "users": safe_int(protocol.get("users")),
                "volume": 0,
                "transactions": 0,
                "balance": safe_float(protocol.get("tvl")),
                "change_1d": safe_float(protocol.get("change_1d")),
                "change_7d": safe_float(protocol.get("change_7d")),
                "change_1m": safe_float(protocol.get("change_1m")),
                "mcap": safe_float(protocol.get("mcap")),
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": [],
            "funding": []
        }
        
        # Add protocol symbol and token info
        if protocol.get("symbol"):
            record["tokens"].append({
                "name": protocol["name"],
                "symbol": protocol["symbol"],
                "format": "ERC-20"  # Default assumption
            })
        
        # Extract additional data from description
        if protocol.get("description"):
            record["description"] = protocol["description"]
            # Simple heuristics for decentralization level
            desc_lower = protocol["description"].lower()
            if any(word in desc_lower for word in ["dao", "decentralized", "governance token"]):
                record["decentralisation_lvl"] = "high"
            elif any(word in desc_lower for word in ["centralized", "team", "company"]):
                record["decentralisation_lvl"] = "low"
            else:
                record["decentralisation_lvl"] = "medium"
        
        # Add URL and social links
        if protocol.get("url"):
            record["website"] = protocol["url"]
        if protocol.get("twitter"):
            record["twitter"] = protocol["twitter"]
        if protocol.get("discord"):
            record["discord"] = protocol["discord"]
        
        # Merge detailed data if available
        if detailed_data:
            record.update(detailed_data)
        
        records.append(record)
        
        # Rate limiting
        time.sleep(0.1)

    return records

def get_protocol_details(slug):
    """
    Get detailed information for a specific protocol
    """
    try:
        # Get protocol specific data
        detail_resp = requests.get(f"https://api.llama.fi/protocol/{slug}")
        if detail_resp.status_code == 200:
            detail_data = detail_resp.json()
            
            details = {}
            
            # Extract launch date if available
            if detail_data.get("inception"):
                try:
                    details["birth_date"] = datetime.fromtimestamp(detail_data["inception"]).date()
                except:
                    pass
            
            # Extract governance information
            governance = []
            if detail_data.get("governance"):
                governance.append("DAO")
            details["governance"] = governance
            
            # Extract audit information
            if detail_data.get("audits"):
                details["audited"] = True
                details["audit_count"] = len(detail_data["audits"])
            
            # Extract additional metrics from chainTvls
            additional_metrics = {}
            if detail_data.get("chainTvls"):
                chain_tvls = detail_data["chainTvls"]
                for chain, tvl_data in chain_tvls.items():
                    if isinstance(tvl_data, dict) and "tvl" in tvl_data:
                        additional_metrics[f"tvl_{chain.lower()}"] = float(tvl_data["tvl"][-1]["totalLiquidityUSD"]) if tvl_data["tvl"] else 0
            
            if additional_metrics:
                if "metrics" not in details:
                    details["metrics"] = {}
                details["metrics"].update(additional_metrics)
            
            return details
            
    except Exception as e:
        print(f"Error fetching details for protocol {slug}: {e}")
        return {}
    
    return {}

def get_protocol_yields(slug):
    """
    Get yield/APY information for a protocol
    """
    try:
        yield_resp = requests.get(f"https://yields.llama.fi/pools/{slug}")
        if yield_resp.status_code == 200:
            yield_data = yield_resp.json()
            return yield_data.get("data", [])
    except Exception as e:
        print(f"Error fetching yields for protocol {slug}: {e}")
    return []

def get_protocol_fees(slug):
    """
    Get fee information for a protocol
    """
    try:
        fees_resp = requests.get(f"https://api.llama.fi/summary/fees/{slug}")
        if fees_resp.status_code == 200:
            fees_data = fees_resp.json()
            return fees_data
    except Exception as e:
        print(f"Error fetching fees for protocol {slug}: {e}")
    return {}

def get_protocol_treasury(slug):
    """
    Get treasury information for a protocol
    """
    try:
        treasury_resp = requests.get(f"https://api.llama.fi/treasury/{slug}")
        if treasury_resp.status_code == 200:
            treasury_data = treasury_resp.json()
            return treasury_data
    except Exception as e:
        print(f"Error fetching treasury for protocol {slug}: {e}")
    return {}
