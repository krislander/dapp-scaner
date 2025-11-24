import sys
import os
import csv
from datetime import datetime
from configparser import ConfigParser
import psycopg2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
DB_NAME = _cfg["database"]["name"]
SUPERUSER = _cfg["database"]["user"]
PASSWORD = _cfg["database"]["password"]
HOST = _cfg["database"]["host"]
PORT = _cfg["database"]["port"]

def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

def export_pilot_dataset_base(output_file="pilot_dataset_base.csv"):
    """Export all DApps without completeness scoring, ordered by name"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Get all DApp data without completeness scoring
    main_query = """
    SELECT 
        d.id,
        d.name,
        c.name as category,
        d.sub_category,
        d.is_active,
        d.multi_chain,
        d.governance_type,
        d.ownership_status,
        d.level_of_decentralisation,
        d.research_comments,
        d.tags,
        d.token_symbol,
        d.token_format,
        d.website,
        d.birth_date as launch_date,
        d.chains,
        COALESCE(
            (SELECT SUM(r.amount) 
             FROM raises r 
             WHERE r.dapp_id = d.id AND r.amount IS NOT NULL), 
            0
        ) as raised_capital,
        d.tvl,
        d.tvl_ratio,
        d.mcap as market_cap,
        d.circulating_supply,
        d.total_supply,
        d.price,
        d.users,
        d.volume,
        d.transactions,
        d.percent_change_1h,
        d.percent_change_24h,
        d.percent_change_7d,
        d.percent_change_30d,
        d.percent_change_60d,
        d.percent_change_90d
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
    ORDER BY d.name;
    """
    
    cur.execute(main_query)
    main_rows = cur.fetchall()
    
    if not main_rows:
        print("No DApps found in database")
        return 0
    
    # Get DApp IDs for TVL historical queries
    dapp_ids = [row[0] for row in main_rows]
    
    # Get most recent TVL historical data for these DApps
    tvl_historical_query = """
    SELECT DISTINCT ON (dapp_id)
        dapp_id,
        total_liquidity_usd
    FROM tvl_historical 
    WHERE dapp_id = ANY(%s)
    ORDER BY dapp_id, date DESC;
    """
    
    cur.execute(tvl_historical_query, (dapp_ids,))
    tvl_historical_data = dict(cur.fetchall())
    
    # Build headers with governance, decentralization, and metrics
    headers = [
        'name', 'dapp_category', 'sub_category', 'is_active', 'is_multi_chain', 'governance_type',
        'ownership_status', 'level_of_decentralisation', 'research_comments', 'tags', 
        'token_symbol', 'token_format', 'website', 'launch_date', 'chains',
        'raised_capital', 'tvl', 'tvl_ratio', 'market_cap', 'circulating_supply', 
        'total_supply', 'price', 'users', 'volume', 'transactions', 'total_liquidity_usd',
        'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 
        'percent_change_60d', 'percent_change_90d'
    ]
    
    # Build output rows
    output_rows = []
    for row in main_rows:
        dapp_id = row[0]
        
        # Basic row data (excluding id)
        output_row = list(row[1:])  # Skip id (first)
        
        # Add TVL historical data
        output_row.append(tvl_historical_data.get(dapp_id, ''))
        
        output_rows.append(output_row)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(output_rows)
    
    cur.close()
    conn.close()
    
    # Print summary
    print(f"✅ Exported {len(output_rows)} DApps to {output_file}")
    
    # Count by category
    category_counts = {}
    for row in output_rows:
        category = row[1]  # dapp_category column
        if category:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    print("📊 Dataset Breakdown:")
    for category, count in sorted(category_counts.items()):
        print(f"  • {category}: {count} DApps")
    
    if len(output_rows) > 0:
        print(f"  • DApps with TVL historical data: {len(tvl_historical_data)}")
        
        # Count non-empty chains
        chains_count = sum(1 for row in output_rows if row[14])  # chains is at index 14
        print(f"  • DApps with chains data: {chains_count}")
    
    return len(output_rows)

def export_raises_data_base(output_file="dapp_raises_base.csv"):
    """Export all raises/funding data from the raises table"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Query to get all raises data with DApp names
    raises_query = """
    SELECT 
        r.id,
        d.name as dapp_name,
        d.slug as dapp_slug,
        c.name as dapp_category,
        r.date,
        r.name as round_name,
        r.round,
        r.amount,
        r.chains,
        r.sector,
        r.category,
        r.category_group,
        r.source,
        r.lead_investors,
        r.other_investors,
        r.valuation,
        r.defillama_id,
        r.created_at
    FROM raises r
    LEFT JOIN dapps d ON r.dapp_id = d.id
    LEFT JOIN categories c ON d.category_id = c.id
    ORDER BY d.name, r.date DESC, r.amount DESC;
    """
    
    cur.execute(raises_query)
    rows = cur.fetchall()
    
    if not rows:
        print("No raises data found in database")
        return 0
    
    # Headers for raises CSV
    headers = [
        'id', 'dapp_name', 'dapp_slug', 'dapp_category', 'date', 'round_name', 'round', 'amount',
        'chains', 'sector', 'category', 'category_group', 'source', 'lead_investors', 
        'other_investors', 'valuation', 'defillama_id', 'created_at'
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    
    cur.close()
    conn.close()
    
    # Print summary
    print(f"✅ Exported {len(rows)} funding rounds to {output_file}")
    
    # Count by DApp
    dapp_counts = {}
    total_funding = 0
    for row in rows:
        dapp_name = row[1]  # dapp_name column
        amount = row[7]     # amount column
        
        if dapp_name:
            dapp_counts[dapp_name] = dapp_counts.get(dapp_name, 0) + 1
        
        if amount and amount > 0:
            total_funding += float(amount)
    
    print("📊 Raises Data Summary:")
    print(f"  • Total funding rounds: {len(rows)}")
    print(f"  • Unique DApps with funding: {len(dapp_counts)}")
    print(f"  • Total funding amount: ${total_funding:,.0f}")
    
    # Top 5 DApps by number of rounds
    top_dapps = sorted(dapp_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("  • Top DApps by funding rounds:")
    for dapp, count in top_dapps:
        print(f"    - {dapp}: {count} rounds")
    
    return len(rows)

if __name__ == "__main__":
    print("📤 Exporting DApp data (Base - No Completeness Scoring)...")
    print("=" * 60)
    
    # Export main dataset
    dapp_count = export_pilot_dataset_base("pilot_dataset_base.csv")
    print()
    
    # Export raises data
    raises_count = export_raises_data_base("dapp_raises_base.csv")
    
    print(f"\n🎉 Export complete!")
    print(f"📊 Summary:")
    print(f"  • {dapp_count} DApps exported to pilot_dataset_base.csv")
    print(f"  • {raises_count} funding rounds exported to dapp_raises_base.csv")
    print("\n💡 Tip: Compare with pilot_dataset.csv and dapp_raises.csv to see differences")

