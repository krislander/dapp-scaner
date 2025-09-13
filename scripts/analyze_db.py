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
        SELECT d.name, d.tvl 
        FROM dapps d
        WHERE d.tvl > 0
        ORDER BY d.tvl DESC
        LIMIT 10;
    """)
    tvl_results = cur.fetchall()
    if tvl_results:
        print(f"\n💰 Top by TVL:")
        for name, tvl in tvl_results:
            print(f"  • {name}: ${tvl:,.0f}")
    
    # Top by Market Cap
    cur.execute("""
        SELECT d.name, d.market_cap 
        FROM dapps d
        WHERE d.market_cap > 0
        ORDER BY d.market_cap DESC
        LIMIT 10;
    """)
    market_cap_results = cur.fetchall()
    if market_cap_results:
        print(f"\n📈 Top by Market Cap:")
        for name, market_cap in market_cap_results:
            print(f"  • {name}: ${market_cap:,.0f}")
    
    # Top by Users
    cur.execute("""
        SELECT d.name, d.users 
        FROM dapps d
        WHERE d.users > 0
        ORDER BY d.users DESC
        LIMIT 10;
    """)
    users_results = cur.fetchall()
    if users_results:
        print(f"\n👥 Top by Users:")
        for name, users in users_results:
            print(f"  • {name}: {users:,.0f}")
    
    # Data completeness
    cur.execute("""
        SELECT 
            COUNT(*) as total_dapps,
            COUNT(CASE WHEN tvl > 0 THEN 1 END) as with_tvl,
            COUNT(CASE WHEN users > 0 THEN 1 END) as with_users,
            COUNT(CASE WHEN market_cap > 0 THEN 1 END) as with_market_cap,
            COUNT(CASE WHEN price > 0 THEN 1 END) as with_price,
            COUNT(CASE WHEN volume > 0 THEN 1 END) as with_volume
        FROM dapps;
    """)
    total_dapps, with_tvl, with_users, with_market_cap, with_price, with_volume = cur.fetchone()
    
    print(f"\n💎 Data Completeness:")
    print(f"  • With TVL: {with_tvl}/{total_dapps} ({with_tvl/total_dapps*100:.1f}%)")
    print(f"  • With Users: {with_users}/{total_dapps} ({with_users/total_dapps*100:.1f}%)")
    print(f"  • With Market Cap: {with_market_cap}/{total_dapps} ({with_market_cap/total_dapps*100:.1f}%)")
    print(f"  • With Price: {with_price}/{total_dapps} ({with_price/total_dapps*100:.1f}%)")
    print(f"  • With Volume: {with_volume}/{total_dapps} ({with_volume/total_dapps*100:.1f}%)")
    
    # Recent additions
    cur.execute("""
        SELECT d.name, c.name as category, d.chains, d.created_at
        FROM dapps d
        LEFT JOIN categories c ON d.category_id = c.id
        ORDER BY d.created_at DESC 
        LIMIT 5;
    """)
    print(f"\n🕒 Recent Additions:")
    for name, category, chains, created_at in cur.fetchall():
        category_str = category if category else "Uncategorized"
        chains_str = chains if chains else "N/A"
        print(f"  • {name} ({category_str}) - {chains_str}")
    
    # Governance analysis
    cur.execute("""
        SELECT governance_type, COUNT(*) 
        FROM dapps 
        WHERE governance_type IS NOT NULL 
        GROUP BY governance_type 
        ORDER BY COUNT(*) DESC;
    """)
    governance_results = cur.fetchall()
    if governance_results:
        print(f"\n🏛️ Governance Types:")
        for gov_type, count in governance_results:
            print(f"  • {gov_type}: {count}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    analyze_database() 