import requests
from datetime import datetime
import time

from dapp_scraper.utils import make_rate_limited_request

def fetch_single_project_defillama(project_name, project_slug=None):
    """
    Fetch data for a single project from DeFiLlama API
    Args:
        project_name: Name of the project/DApp
        project_slug: Slug of the project if known
    Returns:
        dict: Enriched project data with tvl_historical and raises data or None if not found
    """
    try:
        # Helper function for safe numeric conversion
        def safe_numeric(value, default=0):
            """Safely convert value to numeric, handling dicts and other types"""
            if value is None:
                return default
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
            # If it's a dict or other type, return default
            return default
        
        # Try to find the project by slug first
        if project_slug:
            slug_to_try = project_slug
        else:
            # Convert name to likely slug format
            slug_to_try = project_name.lower().replace(" ", "-").replace(".", "")
        
        # Get protocol specific data
        detail_resp = make_rate_limited_request(f"https://api.llama.fi/protocol/{slug_to_try}", headers={}, params={})
        if detail_resp.status_code == 200:
            detail_data = detail_resp.json()
            
            enriched_data = {
                "slug": detail_data.get("slug"),
                "name": detail_data.get("name"),
                "category": detail_data.get("category"),
                "tvl": safe_numeric(detail_data.get("tvl"), 0),
                "change_1d": safe_numeric(detail_data.get("change_1d"), 0),
                "change_7d": safe_numeric(detail_data.get("change_7d"), 0),
                "change_1m": safe_numeric(detail_data.get("change_1m"), 0),
                "mcap": safe_numeric(detail_data.get("mcap"), 0),
                "volume": safe_numeric(detail_data.get("volume"), 0),
            }
            
            # Extract chain information
            if detail_data.get("chains"):
                enriched_data["defillama_chains"] = detail_data["chains"]
            
            # Extract additional metrics from chainTvls
            if detail_data.get("chainTvls"):
                chain_tvls = detail_data["chainTvls"]
                for chain, tvl_data in chain_tvls.items():
                    if isinstance(tvl_data, dict) and "tvl" in tvl_data and tvl_data["tvl"]:
                        try:
                            last_tvl = tvl_data["tvl"][-1]["totalLiquidityUSD"]
                            enriched_data[f"defillama_tvl_{chain.lower()}"] = safe_numeric(last_tvl, 0)
                        except (KeyError, IndexError, TypeError):
                            enriched_data[f"defillama_tvl_{chain.lower()}"] = 0
            
            # Extract TVL historical data
            tvl_historical = []
            if detail_data.get("tvl"):
                for tvl_entry in detail_data["tvl"]:
                    if isinstance(tvl_entry, dict) and "date" in tvl_entry and "totalLiquidityUSD" in tvl_entry:
                        try:
                            tvl_historical.append({
                                "date": datetime.fromtimestamp(tvl_entry["date"]).date(),
                                "total_liquidity_usd": safe_numeric(tvl_entry["totalLiquidityUSD"], 0)
                            })
                        except (ValueError, TypeError, OSError):
                            # Skip invalid entries
                            continue
            enriched_data["tvl_historical"] = tvl_historical
            
            # Extract raises data
            raises = []
            if detail_data.get("raises"):
                for raise_entry in detail_data["raises"]:
                    if isinstance(raise_entry, dict):
                        # Convert chains list to comma-separated string
                        chains_str = ", ".join(raise_entry.get("chains", [])) if raise_entry.get("chains") else ""
                        
                        # Convert investor arrays to comma-separated strings
                        lead_investors_str = ", ".join(raise_entry.get("leadInvestors", [])) if raise_entry.get("leadInvestors") else ""
                        other_investors_str = ", ".join(raise_entry.get("otherInvestors", [])) if raise_entry.get("otherInvestors") else ""
                        
                        raises.append({
                            "date": datetime.fromtimestamp(raise_entry["date"]).date() if raise_entry.get("date") else None,
                            "name": raise_entry.get("name", ""),
                            "round": raise_entry.get("round", ""),
                            "amount": safe_numeric(raise_entry.get("amount"), 0),
                            "chains": chains_str,
                            "sector": raise_entry.get("sector", ""),
                            "category": raise_entry.get("category", ""),
                            "category_group": raise_entry.get("categoryGroup", ""),
                            "source": raise_entry.get("source", ""),
                            "lead_investors": lead_investors_str,
                            "other_investors": other_investors_str,
                            "valuation": safe_numeric(raise_entry.get("valuation"), 0) if raise_entry.get("valuation") else None,
                            "defillama_id": str(raise_entry.get("defillamaId", "")) if raise_entry.get("defillamaId") else ""
                        })
            enriched_data["raises"] = raises
            
            return enriched_data
        
        return None
        
    except Exception as e:
        print(f"❌ Error fetching DeFiLlama data for {project_name}: {e}")
        return None
