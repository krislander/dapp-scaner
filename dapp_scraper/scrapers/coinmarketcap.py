import requests
from configparser import ConfigParser
import os
from datetime import datetime
import time

# Load API key and base URL
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
API_KEY = _cfg["coinmarketcap"]["api_key"]
API_ORIGIN = _cfg["coinmarketcap"]["api_origin"]

def fetch_coinmarketcap(limit):
    """
    Fetch comprehensive cryptocurrency and exchange data from CoinMarketCap API using multiple endpoints
    and normalize to our schema with comprehensive data
    """
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    
    records = []
    
    try:
        # 1. Fetch cryptocurrency listings (main data source)
        crypto_data = fetch_cryptocurrency_listings(headers, limit)
        
        # 2. Fetch exchange listings (use smaller portion of limit)
        exchange_limit = max(10, min(limit // 4, 50))  # Use 1/4 of limit, min 10, max 50
        exchange_data = fetch_exchange_listings(headers, exchange_limit)
        
        # 3. Try to fetch DEX data with network parameters (fallback if fails)
        dex_limit = max(5, min(limit // 8, 20))  # Use 1/8 of limit, min 5, max 20
        dex_data = fetch_dex_data_with_networks(headers, dex_limit)
        
        # Process and merge all data sources
        records = process_and_merge_data(crypto_data, exchange_data, dex_data)
        
        if not records:
            print("⚠️ No data retrieved from any CoinMarketCap endpoint")
            return get_sample_coinmarketcap_data(limit)
        
    except Exception as e:
        print(f"❌ CoinMarketCap API error: {e}")
        print("🔄 Using fallback sample data instead")
        return get_sample_coinmarketcap_data(limit)
    
    return records

def fetch_cryptocurrency_listings(headers, limit):
    """
    Fetch cryptocurrency listings (main data source)
    """
    try:
        url = f"{API_ORIGIN}/v1/cryptocurrency/listings/latest"
        params = {"limit": limit, "sort": "market_cap"}
        
        print(f"Making request to: {url}")
        resp = requests.get(url, headers=headers, params=params)
        
        if resp.status_code != 200:
            print(f"Cryptocurrency listings error: {resp.status_code} - {resp.text[:500]}")
            return []
            
        data = resp.json()
        return data.get("data", [])
        
    except Exception as e:
        print(f"Error fetching cryptocurrency listings: {e}")
        return []

def fetch_exchange_listings(headers, limit):
    """
    Fetch exchange listings using the correct endpoint
    """
    try:
        url = f"{API_ORIGIN}/v1/exchange/listings/latest"
        params = {"limit": limit, "sort": "volume_24h"}
        
        print(f"Making request to: {url}")
        resp = requests.get(url, headers=headers, params=params)
        
        if resp.status_code != 200:
            print(f"Exchange listings error: {resp.status_code} - {resp.text[:500]}")
            return []
            
        data = resp.json()
        return data.get("data", [])
        
    except Exception as e:
        print(f"Error fetching exchange listings: {e}")
        return []

def fetch_dex_data_with_networks(headers, limit):
    """
    Fetch DEX data with network parameters (try multiple networks)
    """
    dex_data = []
    
    # Popular networks to try
    networks = ['ethereum', 'bsc', 'polygon', 'arbitrum', 'avalanche']
    
    for network in networks[:2]:  # Only try first 2 networks to avoid rate limits
        try:
            # Try DEX listings for this network
            dex_listings = fetch_dex_listings_for_network(headers, network, limit // len(networks))
            if dex_listings:
                dex_data.extend(dex_listings)
            time.sleep(1)  # Rate limiting between network calls
        except Exception as e:
            print(f"Error fetching DEX data for {network}: {e}")
            continue
    
    return dex_data

def fetch_dex_listings_for_network(headers, network, limit):
    """
    Fetch DEX listings for a specific network
    """
    try:
        url = f"{API_ORIGIN}/v4/dex/listings/quotes"
        params = {"network": network, "limit": limit}
        
        print(f"Making request to: {url} for network: {network}")
        resp = requests.get(url, headers=headers, params=params)
        
        if resp.status_code != 200:
            print(f"DEX listings error for {network}: {resp.status_code} - {resp.text[:300]}")
            return []
            
        data = resp.json()
        return data.get("data", [])
        
    except Exception as e:
        print(f"Error fetching DEX listings for {network}: {e}")
        return []

def process_and_merge_data(crypto_data, exchange_data, dex_data):
    """
    Process and merge data from all endpoints into our standard schema
    """
    records = []
    
    # Process cryptocurrency data as primary source
    for i, crypto in enumerate(crypto_data):
        print(f"Processing Cryptocurrency {i+1}/{len(crypto_data)}: {crypto.get('name', 'Unknown')}")
        
        record = create_record_from_crypto_data(crypto)
        if record:
            records.append(record)
        
        time.sleep(0.1)  # Rate limiting
    
    # Process exchange data
    for i, exchange in enumerate(exchange_data):
        print(f"Processing Exchange {i+1}/{len(exchange_data)}: {exchange.get('name', 'Unknown')}")
        
        record = create_record_from_exchange_data(exchange)
        if record:
            records.append(record)
        
        time.sleep(0.1)  # Rate limiting
    
    # Process DEX data if available
    for i, dex in enumerate(dex_data):
        print(f"Processing DEX {i+1}/{len(dex_data)}: {dex.get('name', 'Unknown')}")
        
        record = create_record_from_dex_data(dex)
        if record:
            records.append(record)
        
        time.sleep(0.1)  # Rate limiting
    
    return records

def create_record_from_crypto_data(crypto):
    """
    Create a standardized record from cryptocurrency data
    """
    try:
        # Safe value extraction
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
        
        # Extract quote data
        quote_data = crypto.get('quote', {})
        usd_quote = quote_data.get('USD', {}) if quote_data else {}
        
        # Create record
        record = {
            "name": crypto.get('name', 'Unknown'),
            "slug": crypto.get('slug', crypto.get('name', 'unknown').lower().replace(' ', '-')),
            "category": "Cryptocurrency",
            "chains": [crypto.get('platform', {}).get('name', 'Bitcoin')] if crypto.get('platform') else ["Bitcoin"],
            "status": "active",
            "multi_chain": False,  # Most individual cryptocurrencies are single-chain
            "birth_date": None,
            "ownership_status": "Decentralized",  # Default assumption for cryptocurrencies
            "capital_raised": 0,
            "showcase_fun": True,
            "decentralisation_lvl": "high",  # Default assumption for cryptocurrencies
            "industry": "Cryptocurrency",
            "metrics": {
                "tvl": 0,  # Not applicable for individual cryptocurrencies
                "users": 0,  # Not available
                "volume": safe_float(usd_quote.get('volume_24h')),
                "transactions": 0,  # Not available in this endpoint
                "balance": 0,  # Not applicable
                "price": safe_float(usd_quote.get('price')),
                "change_1h": safe_float(usd_quote.get('percent_change_1h')),
                "change_24h": safe_float(usd_quote.get('percent_change_24h')),
                "change_7d": safe_float(usd_quote.get('percent_change_7d')),
                "market_cap": safe_float(usd_quote.get('market_cap')),
                "volume_change_24h": safe_float(usd_quote.get('volume_change_24h')),
                "circulating_supply": safe_float(crypto.get('circulating_supply')),
                "total_supply": safe_float(crypto.get('total_supply')),
                "max_supply": safe_float(crypto.get('max_supply')),
                "market_cap_dominance": safe_float(usd_quote.get('market_cap_dominance')),
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": ["Trading", "Store of Value"],
            "funding": []
        }
        
        # Add token information
        if crypto.get('symbol'):
            record["tokens"].append({
                "name": crypto.get('name'),
                "symbol": crypto.get('symbol'),
                "format": crypto.get('platform', {}).get('token_standard', 'Native') if crypto.get('platform') else 'Native'
            })
        
        # Add launch date if available
        if crypto.get('date_added'):
            try:
                record["birth_date"] = datetime.strptime(crypto.get('date_added')[:10], '%Y-%m-%d').date()
            except:
                pass
        
        # Add platform information
        if crypto.get('platform'):
            platform = crypto.get('platform')
            record["description"] = f"Token on {platform.get('name', 'Unknown')} platform"
            if platform.get('name'):
                record["chains"] = [platform.get('name')]
        
        return record
        
    except Exception as e:
        print(f"Error creating record from crypto data: {e}")
        return None

def create_record_from_exchange_data(exchange):
    """
    Create a standardized record from exchange data
    """
    try:
        # Safe value extraction
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
        
        # Extract quote data
        quote_data = exchange.get('quote', {})
        usd_quote = quote_data.get('USD', {}) if quote_data else {}
        
        record = {
            "name": exchange.get('name', 'Unknown Exchange'),
            "slug": exchange.get('slug', exchange.get('name', 'unknown').lower().replace(' ', '-')),
            "category": "Exchange",
            "chains": [],  # Exchanges typically support multiple chains
            "status": "active",
            "multi_chain": True,  # Most exchanges support multiple chains
            "birth_date": None,
            "ownership_status": "Centralized",  # Most exchanges are centralized
            "capital_raised": 0,
            "showcase_fun": False,
            "decentralisation_lvl": "low",  # Most exchanges are centralized
            "industry": "Exchange",
            "metrics": {
                "tvl": 0,  # Not applicable for exchanges
                "users": 0,  # Not available
                "volume": safe_float(usd_quote.get('volume_24h')),
                "transactions": 0,  # Not available
                "balance": 0,  # Not applicable
                "market_cap": 0,  # Not applicable for exchanges
                "change_24h": safe_float(usd_quote.get('percent_change_24h')),
                "volume_change_24h": safe_float(usd_quote.get('volume_change_24h')),
                "num_market_pairs": safe_int(exchange.get('num_market_pairs')),
                "traffic_score": safe_float(exchange.get('traffic_score')),
                "liquidity_score": safe_float(exchange.get('liquidity_score')),
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": ["Exchange", "Trading"],
            "funding": []
        }
        
        # Add exchange-specific information
        if exchange.get('website'):
            record["website"] = exchange.get('website')
        
        if exchange.get('description'):
            record["description"] = exchange.get('description')
        
        # Add launch date if available
        if exchange.get('date_launched'):
            try:
                record["birth_date"] = datetime.strptime(exchange.get('date_launched')[:10], '%Y-%m-%d').date()
            except:
                pass
        
        return record
        
    except Exception as e:
        print(f"Error creating record from exchange data: {e}")
        return None

def create_record_from_dex_data(dex):
    """
    Create a standardized record from DEX data
    """
    try:
        # Safe value extraction
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
        
        # Extract quote data
        quote_data = dex.get('quote', {})
        usd_quote = quote_data.get('USD', {}) if quote_data else {}
        
        record = {
            "name": dex.get('name', 'Unknown DEX'),
            "slug": dex.get('slug', dex.get('name', 'unknown').lower().replace(' ', '-')),
            "category": "DeFi",
            "chains": [dex.get('network', 'Unknown')],
            "status": "active",
            "multi_chain": False,
            "birth_date": None,
            "ownership_status": "Decentralized",
            "capital_raised": 0,
            "showcase_fun": True,
            "decentralisation_lvl": "high",
            "industry": "DeFi",
            "metrics": {
                "tvl": safe_float(dex.get('total_value_locked')),
                "users": 0,  # Not available
                "volume": safe_float(usd_quote.get('volume_24h')),
                "transactions": safe_int(dex.get('transactions_24h')),
                "balance": safe_float(dex.get('total_value_locked')),
                "price": safe_float(usd_quote.get('price')),
                "change_24h": safe_float(usd_quote.get('percent_change_24h')),
                "market_cap": safe_float(usd_quote.get('market_cap')),
                "volume_change_24h": safe_float(usd_quote.get('volume_change_24h')),
                "num_market_pairs": safe_int(dex.get('num_market_pairs')),
            },
            "tokens": [],
            "protocols": [],
            "fees": [],
            "governance": ["DAO"],  # DEXs typically use DAO governance
            "activities": ["DEX", "Trading", "DeFi"],
            "funding": []
        }
        
        # Add DEX-specific information
        if dex.get('website'):
            record["website"] = dex.get('website')
        
        if dex.get('description'):
            record["description"] = dex.get('description')
        
        # Add typical DEX fee structure
        record["fees"].append({
            "type": "Trading Fee",
            "rate": 0.003,  # Typical 0.3% for most DEXs
            "charged_to": "Traders",
            "recipient": "Liquidity Providers"
        })
        
        return record
        
    except Exception as e:
        print(f"Error creating record from DEX data: {e}")
        return None

def get_sample_coinmarketcap_data(limit):
    """
    Fallback sample data when CoinMarketCap API fails
    """
    sample_data = [
        {
            "name": "Bitcoin",
            "slug": "bitcoin",
            "category": "Cryptocurrency",
            "industry": "Cryptocurrency",
            "chains": ["Bitcoin"],
            "status": "active",
            "multi_chain": False,
            "birth_date": datetime(2009, 1, 3).date(),
            "ownership_status": "Decentralized",
            "capital_raised": 0,
            "showcase_fun": True,
            "decentralisation_lvl": "high",
            "metrics": {
                "tvl": 0,
                "users": 100000000,
                "volume": 15000000000,
                "transactions": 0,
                "balance": 0,
                "price": 43500.75,
                "change_24h": 2.1,
                "market_cap": 855000000000,
            },
            "tokens": [{
                "name": "Bitcoin",
                "symbol": "BTC",
                "format": "Native"
            }],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": ["Trading", "Store of Value"],
            "funding": []
        },
        {
            "name": "Ethereum",
            "slug": "ethereum",
            "category": "Cryptocurrency",
            "industry": "Cryptocurrency",
            "chains": ["Ethereum"],
            "status": "active",
            "multi_chain": False,
            "birth_date": datetime(2015, 7, 30).date(),
            "ownership_status": "Decentralized",
            "capital_raised": 0,
            "showcase_fun": True,
            "decentralisation_lvl": "high",
            "metrics": {
                "tvl": 0,
                "users": 50000000,
                "volume": 8000000000,
                "transactions": 0,
                "balance": 0,
                "price": 2450.30,
                "change_24h": 1.8,
                "market_cap": 295000000000,
            },
            "tokens": [{
                "name": "Ethereum",
                "symbol": "ETH",
                "format": "Native"
            }],
            "protocols": [],
            "fees": [],
            "governance": [],
            "activities": ["Trading", "Smart Contracts", "DeFi"],
            "funding": []
        },
        {
            "name": "Binance",
            "slug": "binance",
            "category": "Exchange",
            "industry": "Exchange",
            "chains": [],
            "status": "active",
            "multi_chain": True,
            "birth_date": datetime(2017, 7, 1).date(),
            "ownership_status": "Centralized",
            "capital_raised": 0,
            "showcase_fun": False,
            "decentralisation_lvl": "low",
            "metrics": {
                "tvl": 0,
                "users": 120000000,
                "volume": 25000000000,
                "transactions": 0,
                "balance": 0,
                "num_market_pairs": 2000,
            },
            "tokens": [],
            "protocols": [],
            "fees": [
                {
                    "type": "Maker Fee",
                    "rate": 0.001,
                    "charged_to": "Makers",
                    "recipient": "Exchange"
                },
                {
                    "type": "Taker Fee",
                    "rate": 0.001,
                    "charged_to": "Takers", 
                    "recipient": "Exchange"
                }
            ],
            "governance": [],
            "activities": ["Exchange", "Trading"],
            "funding": []
        }
    ]
    
    return sample_data[:limit] 