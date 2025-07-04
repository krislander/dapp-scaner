import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dapp_scraper.store import get_conn

def analyze_database():
    """Analyze stored DApp data"""
    conn = get_conn()
    cur = conn.cursor()
    
    print("📊 DApp Database Analysis")
    print("=" * 40)
    
    # Total DApps
    cur.execute("SELECT COUNT(*) FROM dapps;")
    total = cur.fetchone()[0]
    print(f"📱 Total DApps: {total}")
    
    # By category
    cur.execute("""
        SELECT c.name, COUNT(d.id) 
        FROM categories c 
        LEFT JOIN dapps d ON c.id = d.category_id 
        GROUP BY c.name 
        ORDER BY COUNT(d.id) DESC 
        LIMIT 10;
    """)
    print(f"\n🏷️ Top Categories:")
    for category, count in cur.fetchall():
        if count > 0:
            print(f"  • {category}: {count}")
    
    # Multi-chain DApps
    cur.execute("SELECT COUNT(*) FROM dapps WHERE multi_chain = true;")
    multi_chain = cur.fetchone()[0]
    print(f"\n🔗 Multi-chain DApps: {multi_chain}")
    
    # Top by TVL
    cur.execute("""
        SELECT d.name, dm.metric_value 
        FROM dapps d
        JOIN dapp_metrics dm ON d.id = dm.dapp_id
        WHERE dm.metric_name = 'tvl' AND dm.metric_value > 0
        ORDER BY dm.metric_value DESC
        LIMIT 10;
    """)
    tvl_results = cur.fetchall()
    if tvl_results:
        print(f"\n💰 Top by TVL:")
        for name, tvl in tvl_results:
            print(f"  • {name}: ${tvl:,.0f}")
    
    # Enrichment status
    cur.execute("""
        SELECT 
            COUNT(DISTINCT d.id) as total_dapps,
            COUNT(DISTINCT CASE WHEN dm.metric_name LIKE 'cmc_%' THEN d.id END) as with_cmc,
            COUNT(DISTINCT CASE WHEN dm.metric_name LIKE 'defillama_%' THEN d.id END) as with_defillama
        FROM dapps d
        LEFT JOIN dapp_metrics dm ON d.id = dm.dapp_id;
    """)
    total_dapps, with_cmc, with_defillama = cur.fetchone()
    
    print(f"\n💎 Enrichment Status:")
    print(f"  • With CMC data: {with_cmc}/{total_dapps}")
    print(f"  • With DeFiLlama data: {with_defillama}/{total_dapps}")
    
    # Recent additions
    cur.execute("""
        SELECT name, category, chains, created_at
        FROM dapp_summary 
        ORDER BY created_at DESC 
        LIMIT 5;
    """)
    print(f"\n🕒 Recent Additions:")
    for name, category, chains, created_at in cur.fetchall():
        print(f"  • {name} ({category}) - {chains}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    analyze_database() 