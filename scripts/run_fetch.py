import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dapp_scraper.scrapers.defillama import fetch_defillama
from dapp_scraper.scrapers.dappradar import fetch_dappradar
from dapp_scraper.scrapers.deepdao import fetch_deepdao
from dapp_scraper.scrapers.coinmarketcap import fetch_coinmarketcap
from dapp_scraper.store import store_records, get_dapp_count, get_recent_dapps
import time

def main():
    """
    Main function to fetch and store DApp data from all sources
    """
    print("🚀 Starting DApp data collection (Simplified Schema)")
    print("=" * 50)
    
    initial_count = get_dapp_count()
    print(f"📊 Starting with {initial_count} DApps in database")
    
    total_stored = 0
    
    # 1. Fetch from DeFiLlama
    print("\n📊 Fetching data from DeFiLlama...")
    try:
        dl = fetch_defillama(limit=100)
        if dl:
            print(f"✅ Retrieved {len(dl)} protocols from DeFiLlama")
            store_records(dl)
            total_stored += len(dl)
            print(f"✅ Stored {len(dl)} DeFiLlama protocols")
        else:
            print("⚠️ No data retrieved from DeFiLlama")
    except Exception as e:
        print(f"❌ Error with DeFiLlama: {e}")
    
    # Small delay between API calls
    time.sleep(2)
    
    # 2. Fetch from DappRadar
    print("\n📱 Fetching data from DappRadar...")
    try:
        dr = fetch_dappradar(limit=100)
        if dr:
            print(f"✅ Retrieved {len(dr)} DApps from DappRadar")
            store_records(dr)
            total_stored += len(dr)
            print(f"✅ Stored {len(dr)} DappRadar DApps")
        else:
            print("⚠️ No data retrieved from DappRadar")
    except Exception as e:
        print(f"❌ Error with DappRadar: {e}")
    
    # Small delay
    time.sleep(2)
    
    # 3. Fetch from DeepDAO
    print("\n🏛️ Fetching data from DeepDAO...")
    try:
        dd = fetch_deepdao(limit=100)
        if dd:
            print(f"✅ Retrieved {len(dd)} DAOs from DeepDAO")
            store_records(dd)
            total_stored += len(dd)
            print(f"✅ Stored {len(dd)} DeepDAO organizations")
        else:
            print("⚠️ No data retrieved from DeepDAO")
    except Exception as e:
        print(f"❌ Error with DeepDAO: {e}")
    
    # Small delay
    time.sleep(2)
    
    # 4. Fetch from CoinMarketCap
    print("\n💰 Fetching data from CoinMarketCap...")
    try:
        cmc = fetch_coinmarketcap(limit=50)  # Lower limit due to API restrictions
        if cmc:
            print(f"✅ Retrieved {len(cmc)} DEX pairs and exchanges from CoinMarketCap")
            store_records(cmc)
            total_stored += len(cmc)
            print(f"✅ Stored {len(cmc)} CoinMarketCap records")
        else:
            print("⚠️ No data retrieved from CoinMarketCap")
    except Exception as e:
        print(f"❌ Error with CoinMarketCap: {e}")
    
    final_count = get_dapp_count()
    
    print(f"\n🎉 Data collection complete!")
    print(f"📈 Records processed: {total_stored}")
    print(f"📊 Total DApps in database: {final_count} (was {initial_count})")
    print(f"🔗 Sources: DeFiLlama, DappRadar, DeepDAO, CoinMarketCap")
    
    # Show recent DApps
    print(f"\n📋 Recently updated DApps:")
    recent = get_recent_dapps(5)
    for name, slug, category, chains, updated_at in recent:
        print(f"  • {name} ({category}) - {chains}")

def test_single_source(source_name, limit=3):
    """
    Test a single data source with limited records
    """
    print(f"🧪 Testing {source_name} with limit={limit}")
    
    try:
        if source_name.lower() == "defillama":
            data = fetch_defillama(limit=limit)
        elif source_name.lower() == "dappradar":
            data = fetch_dappradar(limit=limit)
        elif source_name.lower() == "deepdao":
            data = fetch_deepdao(limit=limit)
        elif source_name.lower() == "coinmarketcap" or source_name.lower() == "cmc":
            data = fetch_coinmarketcap(limit=limit)
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

def quick_analysis():
    """Quick analysis of stored data"""
    from dapp_scraper.simple_store import get_conn
    
    conn = get_conn()
    cur = conn.cursor()
    
    print("📊 Quick Database Analysis")
    print("=" * 30)
    
    # Total DApps
    cur.execute("SELECT COUNT(*) FROM dapps;")
    total = cur.fetchone()[0]
    print(f"Total DApps: {total}")
    
    # By category
    cur.execute("""
        SELECT c.name, COUNT(d.id) 
        FROM categories c 
        LEFT JOIN dapps d ON c.id = d.category_id 
        GROUP BY c.name 
        ORDER BY COUNT(d.id) DESC 
        LIMIT 5;
    """)
    print("\nTop Categories:")
    for category, count in cur.fetchall():
        print(f"  • {category}: {count}")
    
    # Multi-chain DApps
    cur.execute("SELECT COUNT(*) FROM dapps WHERE multi_chain = true;")
    multi_chain = cur.fetchone()[0]
    print(f"\nMulti-chain DApps: {multi_chain}")
    
    # Top by TVL
    cur.execute("""
        SELECT d.name, dm.metric_value 
        FROM dapps d
        JOIN dapp_metrics dm ON d.id = dm.dapp_id
        WHERE dm.metric_name = 'tvl' AND dm.metric_value > 0
        ORDER BY dm.metric_value DESC
        LIMIT 5;
    """)
    print("\nTop by TVL:")
    for name, tvl in cur.fetchall():
        print(f"  • {name}: ${tvl:,.0f}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Check if we're running in test mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Test mode - run with limited data
            if len(sys.argv) > 2:
                test_single_source(sys.argv[2])
            else:
                print("🧪 Running in test mode...")
                test_single_source("defillama", 2)
                test_single_source("dappradar", 2)
                test_single_source("deepdao", 2)
        elif sys.argv[1] == "analysis":
            quick_analysis()
        else:
            test_single_source(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    else:
        # Full run
        main() 