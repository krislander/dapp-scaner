import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dapp_scraper.utils import safe_numeric
from dapp_scraper.scrapers.defillama import fetch_single_project_defillama
from dapp_scraper.scrapers.dappradar import fetch_dappradar
from dapp_scraper.scrapers.coinmarketcap import fetch_single_project_coinmarketcap
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

def enrich_database_records():
    """
    Go through each record in database and enrich with CMC and DeFiLlama data
    """
    from dapp_scraper.store import get_conn, combine_tags
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Get all DApps that need enrichment
    cur.execute("""
        SELECT id, name, slug, token_symbol, token_name, tags 
        FROM dapps 
        ORDER BY id
    """)
    
    dapps = cur.fetchall()
    total_dapps = len(dapps)
    enriched_count = 0
    
    print(f"🎯 Enriching {total_dapps} DApps...")
    
    for i, (dapp_id, name, slug, token_symbol, token_name, existing_tags) in enumerate(dapps, 1):
        print(f"[{i}/{total_dapps}] {name}")
        
        enrichment_data = {}
        updated_tags = existing_tags  # Start with existing tags
        
        # Try to get CMC data
        if token_symbol:
            cmc_params = {"symbol": token_symbol}
        else:
            cmc_params = {"slug": slug}
        
        cmc_data = fetch_single_project_coinmarketcap(name, cmc_params)
        if cmc_data:
            # Extract CMC data for direct column updates
            price = cmc_data.get('price', 0)
            volume_24h = cmc_data.get('volume_24h', 0)
            volume_change_24h = cmc_data.get('volume_change_24h', 0)
            percent_change_1h = cmc_data.get('percent_change_1h', 0)
            percent_change_24h = cmc_data.get('percent_change_24h', 0)
            percent_change_7d = cmc_data.get('percent_change_7d', 0)
            percent_change_30d = cmc_data.get('percent_change_30d', 0)
            percent_change_60d = cmc_data.get('percent_change_60d', 0)
            percent_change_90d = cmc_data.get('percent_change_90d', 0)
            market_cap = cmc_data.get('market_cap', 0)
            market_cap_dominance = cmc_data.get('market_cap_dominance', 0)
            fully_diluted_market_cap = cmc_data.get('fully_diluted_market_cap', 0)
            circulating_supply = cmc_data.get('circulating_supply', 0)
            total_supply = cmc_data.get('total_supply', 0)
            max_supply = cmc_data.get('max_supply', 0)
            cmc_rank = cmc_data.get('cmc_rank', 0)
            tvl_ratio = cmc_data.get('tvl_ratio', 0)
            
            # Combine tags from CMC with existing DappRadar tags
            cmc_tags = cmc_data.get('cmc_tags', '')
            if cmc_tags:
                updated_tags = combine_tags(existing_tags, cmc_tags)
            
            # Update dapps table with CMC data
            cur.execute("""
                UPDATE dapps SET
                    price = %s,
                    volume_24h = %s,
                    volume_change_24h = %s,
                    percent_change_1h = %s,
                    percent_change_24h = %s,
                    percent_change_7d = %s,
                    percent_change_30d = %s,
                    percent_change_60d = %s,
                    percent_change_90d = %s,
                    market_cap = %s,
                    market_cap_dominance = %s,
                    fully_diluted_market_cap = %s,
                    circulating_supply = %s,
                    total_supply = %s,
                    max_supply = %s,
                    cmc_rank = %s,
                    tvl_ratio = %s,
                    tags = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (price, volume_24h, volume_change_24h, percent_change_1h, percent_change_24h,
                  percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d,
                  market_cap, market_cap_dominance, fully_diluted_market_cap, circulating_supply, 
                  total_supply, max_supply, cmc_rank, tvl_ratio, updated_tags, dapp_id))
        
        # Try to get DeFiLlama data
        defillama_data = fetch_single_project_defillama(name, slug)
        if defillama_data:            
            tvl = safe_numeric(defillama_data.get('tvl'), 0)
            volume = safe_numeric(defillama_data.get('volume'), 0)
            
            # Update dapps table with DeFiLlama data
            cur.execute("""
                UPDATE dapps SET
                    tvl = %s,
                    volume = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (tvl, volume, dapp_id))
            
            # Store TVL historical data if present
            if defillama_data.get('tvl_historical'):
                from dapp_scraper.store import store_tvl_historical
                store_tvl_historical(cur, dapp_id, defillama_data['tvl_historical'])
            
            # Store raises data if present
            if defillama_data.get('raises'):
                from dapp_scraper.store import store_raises
                store_raises(cur, dapp_id, defillama_data['raises'])
        
        if cmc_data or defillama_data:
            enriched_count += 1
        
        # Small delay between enrichments
        time.sleep(0.2)
    
    conn.commit()
    cur.close()
    conn.close()
    
    return enriched_count

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