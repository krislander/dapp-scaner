import requests
from configparser import ConfigParser
import os

from dapp_scraper.utils import make_rate_limited_request

# Load API key and base URL
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
API_KEY = _cfg["coinmarketcap"]["api_key"]
API_ORIGIN = _cfg["coinmarketcap"]["api_origin"]

def fetch_single_project_coinmarketcap(project_name, token_symbol=None):
    """
    Fetch data for a single project from CoinMarketCap API
    Args:
        project_name: Name of the project/DApp
        token_symbol: Token symbol if available
    Returns:
        dict: Enriched project data or None if not found
    """
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    
    try:
        # Try to find the project by symbol first, then by name
        search_term = token_symbol if token_symbol else project_name
        
        # Search for cryptocurrency
        url = f"{API_ORIGIN}/v1/cryptocurrency/quotes/latest"
        params = {"symbol": search_term} if token_symbol else {"slug": project_name.lower().replace(" ", "-")}
        
        resp = make_rate_limited_request(url, headers=headers, params=params)
        
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            
            if data:
                # Get the first result if searching by symbol
                if token_symbol and isinstance(data, dict):
                    coin_data = list(data.values())[0] if data else None
                else:
                    coin_data = data
                
                if coin_data:
                    # Extract tags
                    tags_list = coin_data.get("tags", [])
                    tags_str = ", ".join([tag.get("name", "") for tag in tags_list if tag.get("name")])
                    
                    # Get full quote USD data
                    quote_usd = coin_data.get("quote", {}).get("USD", {})
                    
                    return {
                        "cmc_id": coin_data.get("id"),
                        "cmc_name": coin_data.get("name"),
                        "cmc_symbol": coin_data.get("symbol"),
                        "cmc_slug": coin_data.get("slug"),
                        "cmc_tags": tags_str,
                        "market_cap": quote_usd.get("market_cap", 0),
                        "price": quote_usd.get("price", 0),
                        "volume_24h": quote_usd.get("volume_24h", 0),
                        "volume_change_24h": quote_usd.get("volume_change_24h", 0),
                        "percent_change_1h": quote_usd.get("percent_change_1h", 0),
                        "percent_change_24h": quote_usd.get("percent_change_24h", 0),
                        "percent_change_7d": quote_usd.get("percent_change_7d", 0),
                        "percent_change_30d": quote_usd.get("percent_change_30d", 0),
                        "percent_change_60d": quote_usd.get("percent_change_60d", 0),
                        "percent_change_90d": quote_usd.get("percent_change_90d", 0),
                        "market_cap_dominance": quote_usd.get("market_cap_dominance", 0),
                        "fully_diluted_market_cap": quote_usd.get("fully_diluted_market_cap", 0),
                        "circulating_supply": coin_data.get("circulating_supply", 0),
                        "total_supply": coin_data.get("total_supply", 0),
                        "max_supply": coin_data.get("max_supply", 0),
                        "cmc_rank": coin_data.get("cmc_rank", 0),
                        "tvl_ratio": coin_data.get("tvl_ratio", 0),
                    }
        
        return None
        
    except Exception as e:
        print(f"❌ Error fetching CMC data for {project_name}: {e}")
        return None 