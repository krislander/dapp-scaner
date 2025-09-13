import sys
import os

# Add project root to Python path first
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.run_fetch_enrich import enrich_database_records

from dapp_scraper.scrapers.dappradar import fetch_dappradar
from dapp_scraper.store import store_records, get_dapp_count, get_recent_dapps
import time

def main(limit):
    """
    Main function to fetch and enrich DApp data
    1. Fetch all DApps from DappRadar and save to DB
    2. Enrich each saved DApp with CMC and DeFiLlama data
    """
    print("🚀 Starting DApp data collection and enrichment")
    
    initial_count = get_dapp_count()
    print(f"📊 Current DApps in database: {initial_count}")
    
    # Phase 1: Fetch DappRadar data
    print("\n📱 Phase 1: Fetching DappRadar data...")
    try:
        dappradar_data = fetch_dappradar(limit)
        if dappradar_data:
            print(f"✅ Retrieved {len(dappradar_data)} DApps from DappRadar")
            store_records(dappradar_data)
            print(f"✅ Saved {len(dappradar_data)} DApps to database")
        else:
            print("❌ No data retrieved from DappRadar")
            return
    except Exception as e:
        print(f"❌ Error with DappRadar: {e}")
        return
    
    # Phase 2: Enrich with CMC and DeFiLlama data
    print("\n💰 Phase 2: Enriching with CMC and DeFiLlama data...")
    enriched_count = enrich_database_records()
    
    final_count = get_dapp_count()
    print(f"\n🎉 Process complete!")
    print(f"📈 DApps processed: {len(dappradar_data) if 'dappradar_data' in locals() else 0}")
    print(f"💎 Records enriched: {enriched_count}")
    print(f"📊 Total DApps in database: {final_count}")

def test_single_source(source_name, limit):
    """
    Test a single data source with specified limit
    """
    print(f"🧪 Testing {source_name} with limit={limit}")
    
    try:
        if source_name.lower() == "dappradar":
            data = fetch_dappradar(limit)
            if data:
                print(f"✅ Retrieved {len(data)} records")
                for i, record in enumerate(data[:5]):  # Show first 5
                    chains = ", ".join(record.get('chains', [])) if record.get('chains') else "N/A"
                    print(f"  {i+1}. {record['name']} ({record.get('category', 'N/A')}) - {chains}")
                
                store_records(data)
                print(f"✅ Stored {len(data)} records")
            else:
                print("⚠️ No data retrieved")
        else:
            print(f"❌ Unknown source: {source_name}")
            
    except Exception as e:
        print(f"❌ Error testing {source_name}: {e}")

def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python run_fetch.py <limit>                    # Fetch and enrich DApps")
    print("  python run_fetch.py test dappradar <limit>     # Test DappRadar fetching")
    print("")
    print("Examples:")
    print("  python run_fetch.py 500                        # Fetch 500 DApps and enrich")
    print("  python run_fetch.py test dappradar 10          # Test with 10 records")

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