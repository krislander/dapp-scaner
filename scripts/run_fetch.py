import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dapp_scraper.scrapers.defillama import fetch_defillama
from dapp_scraper.scrapers.dappradar import fetch_dappradar
from dapp_scraper.scrapers.deepdao import fetch_deepdao
from dapp_scraper.scrapers.coinmarketcap import fetch_coinmarketcap
from dapp_scraper.store import store_records, get_dapp_count, get_recent_dapps
import time

def main(limit):
    """
    Main function to fetch and store DApp data
    Args:
        limit: Number of records to fetch (required)
    """
    
    initial_count = get_dapp_count()
    print(f"📊 Starting with {initial_count} DApps in database")
    print(f"🎯 Target limit: {limit} records")
    
    total_stored = 0
    
    # Only fetch from DappRadar for now
    print(f"\n📱 Fetching data from DappRadar (limit: {limit})...")
    try:
        dr = fetch_dappradar(limit)
        if dr:
            print(f"✅ Retrieved {len(dr)} DApps from DappRadar")
            store_records(dr)
            total_stored += len(dr)
            print(f"✅ Stored {len(dr)} DappRadar DApps")
        else:
            print("⚠️ No data retrieved from DappRadar")
    except Exception as e:
        print(f"❌ Error with DappRadar: {e}")
    
    # Other sources are commented out for now but kept in code
    # # 1. Fetch from DeFiLlama
    # print(f"\n📊 Fetching data from DeFiLlama (limit: {limit})...")
    # try:
    #     dl = fetch_defillama(limit)
    #     if dl:
    #         print(f"✅ Retrieved {len(dl)} protocols from DeFiLlama")
    #         store_records(dl)
    #         total_stored += len(dl)
    #         print(f"✅ Stored {len(dl)} DeFiLlama protocols")
    #     else:
    #         print("⚠️ No data retrieved from DeFiLlama")
    # except Exception as e:
    #     print(f"❌ Error with DeFiLlama: {e}")
    
    # # Small delay between API calls
    # time.sleep(2)
    
    # # 3. Fetch from DeepDAO
    # print(f"\n🏛️ Fetching data from DeepDAO (limit: {limit})...")
    # try:
    #     dd = fetch_deepdao(limit)
    #     if dd:
    #         print(f"✅ Retrieved {len(dd)} DAOs from DeepDAO")
    #         store_records(dd)
    #         total_stored += len(dd)
    #         print(f"✅ Stored {len(dd)} DeepDAO organizations")
    #     else:
    #         print("⚠️ No data retrieved from DeepDAO")
    # except Exception as e:
    #     print(f"❌ Error with DeepDAO: {e}")
    
    # # Small delay
    # time.sleep(2)
    
    # # 4. Fetch from CoinMarketCap
    # print(f"\n💰 Fetching data from CoinMarketCap (limit: {limit})...")
    # try:
    #     cmc = fetch_coinmarketcap(limit)
    #     if cmc:
    #         print(f"✅ Retrieved {len(cmc)} DEX pairs and exchanges from CoinMarketCap")
    #         store_records(cmc)
    #         total_stored += len(cmc)
    #         print(f"✅ Stored {len(cmc)} CoinMarketCap records")
    #     else:
    #         print("⚠️ No data retrieved from CoinMarketCap")
    # except Exception as e:
    #     print(f"❌ Error with CoinMarketCap: {e}")
    
    final_count = get_dapp_count()
    
    print(f"\n🎉 Data collection complete!")
    print(f"📈 Records processed: {total_stored}")
    print(f"📊 Total DApps in database: {final_count} (was {initial_count})")
    
    # Show recent DApps
    print(f"\n📋 Recently updated DApps:")
    recent = get_recent_dapps(5)
    for name, slug, category, chains, updated_at in recent:
        print(f"  • {name} ({category}) - {chains}")

def test_single_source(source_name, limit):
    """
    Test a single data source with specified limit (no default)
    Args:
        source_name: Name of the source to test
        limit: Number of records to fetch (required)
    """
    print(f"🧪 Testing {source_name} with limit={limit}")
    
    try:
        if source_name.lower() == "defillama":
            data = fetch_defillama(limit)
        elif source_name.lower() == "dappradar":
            data = fetch_dappradar(limit)
        elif source_name.lower() == "deepdao":
            data = fetch_deepdao(limit)
        elif source_name.lower() == "coinmarketcap" or source_name.lower() == "cmc":
            data = fetch_coinmarketcap(limit)
        else:
            print(f"❌ Unknown source: {source_name}")
            return
        
        if data:
            print(f"✅ Retrieved {len(data)} records from {source_name}")
            for i, record in enumerate(data):
                chains = ", ".join(record.get('chains', [])) if record.get('chains') else "N/A"
                print(f"  {i+1}. {record['name']} ({record.get('category', 'N/A')}) - {chains}")
            
            # Store the test data
            store_records(data)
            print(f"✅ Successfully stored {len(data)} records")
        else:
            print(f"⚠️ No data retrieved from {source_name}")
            
    except Exception as e:
        print(f"❌ Error testing {source_name}: {e}")


def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python run_fetch.py <limit>                    # Fetch from DappRadar with specified limit")
    print("  python run_fetch.py test <source> <limit>      # Test specific source with limit")
    print("  python run_fetch.py analysis                   # Run database analysis")
    print("")
    print("Examples:")
    print("  python run_fetch.py 500                        # Fetch 500 DApps from DappRadar")
    print("  python run_fetch.py test dappradar 10          # Test DappRadar with 10 records")
    print("  python run_fetch.py analysis                   # Analyze current database")
    print("")
    print("Available sources for testing: dappradar, defillama, deepdao, coinmarketcap")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Limit parameter is required!")
        print_usage()
        sys.exit(1)
    
    if sys.argv[1] == "test":
        if len(sys.argv) < 4:
            print("❌ Error: Test mode requires source name and limit!")
            print("Usage: python run_fetch.py test <source> <limit>")
            sys.exit(1)
        test_single_source(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "help" or sys.argv[1] == "--help":
        print_usage()
    else:
        try:
            limit = int(sys.argv[1])
            if limit <= 0:
                print("❌ Error: Limit must be a positive integer!")
                sys.exit(1)
            main(limit)
        except ValueError:
            print("❌ Error: Limit must be a valid integer!")
            print_usage()
            sys.exit(1) 