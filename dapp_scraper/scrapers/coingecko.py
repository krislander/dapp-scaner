import requests
from configparser import ConfigParser
import os

from dapp_scraper.utils import make_rate_limited_request, safe_numeric

# Load API key and base URL
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))

# CoinGecko uses free public API
try:
    API_KEY = _cfg["coingecko"]["api_key"]
    API_ORIGIN = _cfg["coingecko"]["api_origin"]
except:
    # Fallback to public API if no config
    API_KEY = None
    API_ORIGIN = "https://api.coingecko.com/api/v3"

def fetch_coingecko_public_list():
    """
    Fetch public list of CoinGecko projects
    Returns:
        list: List of CoinGecko projects
    """
    url = f"{API_ORIGIN}/coins/list"
    headers = {}
    if API_KEY:
        headers["x-cg-demo-api-key"] = API_KEY

    try:
        resp = make_rate_limited_request(url, headers=headers, params={})
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception as e:
        print(f"❌ Error fetching CoinGecko public list: {e}")
        return None

def fetch_single_project_coingecko(project_name, params=None):
    """
    Fetch data for a single project from CoinGecko API using gecko_id
    Args:
        project_name: Name of the project/DApp
        params: Dict with gecko_id - {"gecko_id": id}
    Returns:
        dict: Enriched project data or None if not found
    """
    headers = {}
    if API_KEY:
        headers["x-cg-demo-api-key"] = API_KEY
    
    try:
        # Only work with gecko_id parameter
        if not params or "gecko_id" not in params:
            print(f"❌ No gecko_id provided for {project_name}")
            return None
        
        gecko_id = params["gecko_id"]
        url = f"{API_ORIGIN}/coins/{gecko_id}"
        
        resp = make_rate_limited_request(url, headers=headers, params={})
        
        if resp.status_code == 200:
            coin_data = resp.json()
            return parse_coingecko_data(coin_data)
        elif resp.status_code == 404:
            print(f"❌ CoinGecko project not found: {gecko_id}")
        else:
            print(f"❌ CoinGecko API error for {gecko_id}: {resp.status_code}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error fetching CoinGecko data for {project_name}: {e}")
        return None

def parse_coingecko_data(coin_data):
    """
    Parse CoinGecko API response into standardized format
    Args:
        coin_data: Raw CoinGecko API response
    Returns:
        dict: Parsed and standardized data
    """
    try:
        # Extract market data
        market_data = coin_data.get("market_data", {})
        
        # Extract categories/tags
        categories = coin_data.get("categories", [])
        categories_str = ", ".join([cat for cat in categories if cat]) if categories else ""
        
        # Extract links and social data
        links = coin_data.get("links", {})
        
        # Extract platform/contract data
        platforms = coin_data.get("platforms", {})
        
        # Current price data
        current_price = market_data.get("current_price", {})
        price_usd = safe_numeric(current_price.get("usd"), 0)
        
        # Market cap data
        market_cap = market_data.get("market_cap", {})
        market_cap_usd = safe_numeric(market_cap.get("usd"), 0)
        
        # Volume data
        total_volume = market_data.get("total_volume", {})
        total_value_locked = market_data.get("total_value_locked", {})
        tvl = safe_numeric(total_value_locked.get("usd"), 0)
        volume_24h_usd = safe_numeric(total_volume.get("usd"), 0)
        
        # Price change data
        price_change_24h = safe_numeric(market_data.get("price_change_percentage_24h"), 0)
        price_change_7d = safe_numeric(market_data.get("price_change_percentage_7d"), 0)
        price_change_30d = safe_numeric(market_data.get("price_change_percentage_30d"), 0)
        price_change_1y = safe_numeric(market_data.get("price_change_percentage_1y"), 0)
        
        # Supply data
        circulating_supply = safe_numeric(market_data.get("circulating_supply"), 0)
        total_supply = safe_numeric(market_data.get("total_supply"), 0)
        max_supply = safe_numeric(market_data.get("max_supply"), 0)
        
        # Market metrics
        market_cap_rank = safe_numeric(coin_data.get("market_cap_rank"), 0)
        fully_diluted_valuation = market_data.get("fully_diluted_valuation", {})
        fdv_usd = safe_numeric(fully_diluted_valuation.get("usd"), 0)
        
        # Additional metrics
        market_cap_change_24h = safe_numeric(market_data.get("market_cap_change_percentage_24h"), 0)
        
        # Count social media presence
        social_count = 0
        if links.get("homepage"):
            social_count += 1
        if links.get("twitter_screen_name"):
            social_count += 1
        if links.get("telegram_channel_identifier"):
            social_count += 1
        if links.get("repos_url", {}).get("github"):
            social_count += 1
        
        # Add community and developer data if available
        community_data = coin_data.get("community_data", {})
        if community_data.get("reddit_subscribers", 0) > 0:
            social_count += 1
        if community_data.get("telegram_channel_user_count", 0) > 0:
            social_count += 1
            
        # Extract all available links for social count
        announcement_urls = links.get("announcement_url", [])
        if announcement_urls:
            social_count += len([url for url in announcement_urls if url])
        
        return {
            "gecko_id": coin_data.get("id"),
            "gecko_name": coin_data.get("name"),
            "gecko_symbol": coin_data.get("symbol", "").upper(),
            "gecko_categories": categories_str,
            "coingecko_social_count": social_count,
            
            # Price data
            "price": price_usd,
            "price_change_24h": price_change_24h,
            "price_change_7d": price_change_7d,
            "price_change_30d": price_change_30d,
            "price_change_1y": price_change_1y,
            
            # Market data
            "market_cap": market_cap_usd,
            "tvl": tvl,
            "market_cap_rank": market_cap_rank,
            "market_cap_change_24h": market_cap_change_24h,
            "fully_diluted_valuation": fdv_usd,
            
            # Volume data
            "volume_24h": volume_24h_usd,
            
            # Supply data
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
            "max_supply": max_supply,
            
            # Platform/contract data
            "platforms": platforms,
            
            # Raw data for debugging
            "gecko_last_updated": coin_data.get("last_updated"),
        }
        
    except Exception as e:
        print(f"❌ Error parsing CoinGecko data: {e}")
        return None 