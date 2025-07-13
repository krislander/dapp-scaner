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
        dict: Enriched project data or None if not found
    """
    try:
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
                "defillama_slug": detail_data.get("slug"),
                "defillama_name": detail_data.get("name"),
                "defillama_category": detail_data.get("category"),
                "defillama_tvl": detail_data.get("tvl", 0),
                "defillama_change_1d": detail_data.get("change_1d", 0),
                "defillama_change_7d": detail_data.get("change_7d", 0),
                "defillama_change_1m": detail_data.get("change_1m", 0),
                "defillama_mcap": detail_data.get("mcap", 0),
            }
            
            # Extract launch date if available
            if detail_data.get("inception"):
                try:
                    launch_date = datetime.fromtimestamp(detail_data["inception"])
                    enriched_data["defillama_launch_date"] = launch_date.strftime("%Y-%m-%d")
                except:
                    pass
            
            # Extract chain information
            if detail_data.get("chains"):
                enriched_data["defillama_chains"] = detail_data["chains"]
            
            # Extract additional metrics from chainTvls
            if detail_data.get("chainTvls"):
                chain_tvls = detail_data["chainTvls"]
                for chain, tvl_data in chain_tvls.items():
                    if isinstance(tvl_data, dict) and "tvl" in tvl_data and tvl_data["tvl"]:
                        enriched_data[f"defillama_tvl_{chain.lower()}"] = float(tvl_data["tvl"][-1]["totalLiquidityUSD"])
            
            return enriched_data
        
        return None
        
    except Exception as e:
        print(f"❌ Error fetching DeFiLlama data for {project_name}: {e}")
        return None
