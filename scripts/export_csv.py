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

def export_pilot_dataset(output_file="pilot_dataset.csv"):
    """Export 500 DApps with maximum non-null fields including TVL historical data"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # First, get the main DApp data with completeness scoring
    main_query = """
    SELECT 
        d.id,
        d.name,
        c.name as category,
        d.is_active,
        d.multi_chain,
        d.governance_type,
        d.ownership_status,
        d.decentralisation_lvl,
        d.tags,
        d.token_symbol,
        d.token_format,
        d.website,
        d.telegram,
        d.twitter,
        d.discord,
        d.github,
        d.youtube,
        d.instagram,
        d.birth_date as launch_date,
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
        d.percent_change_90d,
        -- Count non-null fields for ordering (prioritize complete records)
        (
            CASE WHEN d.name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN c.name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.tags IS NOT NULL AND d.tags != '' THEN 1 ELSE 0 END +
            CASE WHEN d.ownership_status IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.decentralisation_lvl IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.birth_date IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN (SELECT SUM(r.amount) FROM raises r WHERE r.dapp_id = d.id AND r.amount IS NOT NULL) > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.website IS NOT NULL AND d.website != '' THEN 1 ELSE 0 END +
            CASE WHEN d.telegram IS NOT NULL AND d.telegram != '' THEN 1 ELSE 0 END +
            CASE WHEN d.twitter IS NOT NULL AND d.twitter != '' THEN 1 ELSE 0 END +
            CASE WHEN d.discord IS NOT NULL AND d.discord != '' THEN 1 ELSE 0 END +
            CASE WHEN d.github IS NOT NULL AND d.github != '' THEN 1 ELSE 0 END +
            CASE WHEN d.youtube IS NOT NULL AND d.youtube != '' THEN 1 ELSE 0 END +
            CASE WHEN d.instagram IS NOT NULL AND d.instagram != '' THEN 1 ELSE 0 END +
            CASE WHEN d.token_symbol IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.token_format IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.governance_type IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.tvl IS NOT NULL AND d.tvl > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.tvl_ratio IS NOT NULL AND d.tvl_ratio > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.users IS NOT NULL AND d.users > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.volume IS NOT NULL AND d.volume > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.transactions IS NOT NULL AND d.transactions > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.mcap IS NOT NULL AND d.mcap > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.price IS NOT NULL AND d.price > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.percent_change_24h IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.percent_change_7d IS NOT NULL THEN 1 ELSE 0 END
        ) as completeness_score
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
    ORDER BY completeness_score DESC, d.name
    LIMIT 500;
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
    
    # Build headers with separate token and social media fields
    headers = [
        'name', 'dapp_category', 'is_active', 'is_multi_chain', 'governance_type',
        'ownership_status', 'level_of_decentralisation', 'tags', 
        'token_symbol', 'token_format',
        'website', 'telegram', 'twitter', 'discord', 'github', 'youtube', 'instagram',
        'launch_date', 'raised_capital', 'tvl', 'tvl_ratio', 'market_cap', 'circulating_supply', 
        'total_supply', 'price', 'users', 'volume', 'transactions', 'total_liquidity_usd',
        'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 
        'percent_change_60d', 'percent_change_90d'
    ]
    
    # Build output rows
    output_rows = []
    for row in main_rows:
        dapp_id = row[0]
        
        # Basic row data (excluding id and completeness_score)
        output_row = list(row[1:-1])  # Skip id (first) and completeness_score (last)
        
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
        avg_completeness = sum(main_row[-1] for main_row in main_rows) / len(main_rows)
        print(f"  • Average completeness score: {avg_completeness:.1f}/26 fields")
        print(f"  • DApps with TVL historical data: {len(tvl_historical_data)}")
    
    return len(output_rows)

def export_raises_data(output_file="dapp_raises.csv"):
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
    ORDER BY r.date DESC, d.name, r.amount DESC;
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
    print("📤 Exporting DApp data...")
    print("=" * 40)
    
    # Export main dataset
    dapp_count = export_pilot_dataset("pilot_dataset.csv")
    print()
    
    # Export raises data
    raises_count = export_raises_data("dapp_raises.csv")
    
    print(f"\n🎉 Export complete!")
    print(f"📊 Summary:")
    print(f"  • {dapp_count} DApps exported to pilot_dataset.csv")
    print(f"  • {raises_count} funding rounds exported to dapp_raises.csv") 