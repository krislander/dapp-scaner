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

def export_dapps_to_csv(output_file="dapps_export.csv"):
    """Export all DApps to a single CSV file"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Query to get all DApp data from the new structure
    query = """
    SELECT 
        d.id,
        d.name,
        d.slug,
        c.name as category,
        i.name as industry,
        d.status,
        d.chains,
        d.multi_chain,
        d.ownership_status,
        d.decentralisation_lvl,
        d.birth_date,
        d.capital_raised,
        d.showcase_fun,
        d.token_name,
        d.token_symbol,
        d.token_format,
        d.governance_type,
        d.website,
        d.twitter,
        d.discord,
        d.description,
        d.created_at,
        d.updated_at,
        -- Direct metrics from dapps table
        d.tvl,
        d.users,
        d.volume,
        d.transactions,
        d.market_cap,
        d.circulating_supply,
        d.total_supply,
        d.max_supply,
        d.price,
        d.volume_24h,
        d.volume_change_24h,
        d.percent_change_1h,
        d.percent_change_24h,
        d.percent_change_7d,
        d.percent_change_30d,
        d.market_cap_dominance,
        d.fully_diluted_market_cap
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
    LEFT JOIN industries i ON d.industry_id = i.id
    ORDER BY d.name;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    
    # Column headers
    headers = [
        'id', 'name', 'slug', 'category', 'industry', 'status', 'chains', 'multi_chain',
        'ownership_status', 'decentralisation_lvl', 'birth_date', 'capital_raised', 
        'showcase_fun', 'token_name', 'token_symbol', 'token_format', 'governance_type',
        'website', 'twitter', 'discord', 'description', 'created_at', 'updated_at',
        'tvl', 'users', 'volume', 'transactions', 'market_cap', 'circulating_supply',
        'total_supply', 'max_supply', 'price', 'volume_24h', 'volume_change_24h',
        'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d',
        'market_cap_dominance', 'fully_diluted_market_cap'
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    
    cur.close()
    conn.close()
    
    print(f"✅ Exported {len(rows)} DApps to {output_file}")
    return len(rows)

def export_pilot_dataset(output_file="pilot_dataset.csv"):
    """Export a pilot dataset of 30 DApps with maximum non-null fields from specified categories"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Define target categories
    target_categories = ['games', 'defi', 'collectibles', 'marketplaces', 'high-risk', 'gambling', 'exchanges', 'social', 'other']
    
    # Query to get 30 DApps with most complete data from target categories
    query = """
    SELECT 
        d.id,
        d.name,
        d.slug,
        c.name as category,
        i.name as industry,
        d.status,
        d.chains,
        d.multi_chain,
        d.ownership_status,
        d.decentralisation_lvl,
        d.birth_date,
        d.capital_raised,
        d.showcase_fun,
        d.token_name,
        d.token_symbol,
        d.token_format,
        d.governance_type,
        d.website,
        d.twitter,
        d.discord,
        d.description,
        d.created_at,
        d.updated_at,
        -- Direct metrics from dapps table
        d.tvl,
        d.users,
        d.volume,
        d.transactions,
        d.market_cap,
        d.price,
        d.volume_24h,
        d.percent_change_24h,
        d.percent_change_7d,
        -- Count non-null fields for ordering (prioritize complete records)
        (
            CASE WHEN d.name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN i.name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.chains IS NOT NULL AND d.chains != '' THEN 1 ELSE 0 END +
            CASE WHEN d.ownership_status IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.decentralisation_lvl IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.birth_date IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.capital_raised IS NOT NULL AND d.capital_raised > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.token_name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.token_symbol IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.governance_type IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.website IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.twitter IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.discord IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.description IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.users IS NOT NULL AND d.users > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.volume IS NOT NULL AND d.volume > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.transactions IS NOT NULL AND d.transactions > 0 THEN 1 ELSE 0 END +
            CASE WHEN d.tvl IS NOT NULL AND d.tvl > 0 THEN 1 ELSE 0 END
        ) as completeness_score
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
    LEFT JOIN industries i ON d.industry_id = i.id
    WHERE c.name = ANY(%s)
    ORDER BY completeness_score DESC, d.name
    LIMIT 30;
    """
    
    cur.execute(query, (target_categories,))
    rows = cur.fetchall()
    
    # Column headers (excluding the completeness_score which is just for ordering)
    headers = [
        'id', 'name', 'slug', 'category', 'industry', 'status', 'chains', 'multi_chain',
        'ownership_status', 'decentralisation_lvl', 'birth_date', 'capital_raised', 
        'showcase_fun', 'token_name', 'token_symbol', 'token_format', 'governance_type',
        'website', 'twitter', 'discord', 'description', 'created_at', 'updated_at',
        'tvl', 'users', 'volume', 'transactions', 'market_cap', 'price', 'volume_24h',
        'percent_change_24h', 'percent_change_7d', 'completeness_score'
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    
    cur.close()
    conn.close()
    
    # Print summary by category
    print(f"✅ Exported {len(rows)} DApps to {output_file}")
    
    # Count by category
    category_counts = {}
    for row in rows:
        category = row[3]  # category column
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("📊 Pilot Dataset Breakdown:")
    for category, count in sorted(category_counts.items()):
        print(f"  • {category}: {count} DApps")
    
    if len(rows) > 0:
        avg_completeness = sum(row[-1] for row in rows) / len(rows)  # completeness_score is last column
        print(f"  • Average completeness score: {avg_completeness:.1f}/18 fields")
    
    return len(rows)

def export_summary_stats(output_file="dapp_summary_stats.csv"):
    """Export summary statistics"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Collect various statistics
    stats = []
    
    # Total DApps
    cur.execute("SELECT COUNT(*) FROM dapps;")
    stats.append(['Total DApps', cur.fetchone()[0]])
    
    # By category
    cur.execute("""
        SELECT c.name, COUNT(d.id) 
        FROM categories c 
        LEFT JOIN dapps d ON c.id = d.category_id 
        WHERE d.id IS NOT NULL
        GROUP BY c.name 
        ORDER BY COUNT(d.id) DESC;
    """)
    for category, count in cur.fetchall():
        stats.append([f'DApps in {category}', count])
    
    # Multi-chain DApps
    cur.execute("SELECT COUNT(*) FROM dapps WHERE multi_chain = true;")
    stats.append(['Multi-chain DApps', cur.fetchone()[0]])
    
    # DApps with tokens
    cur.execute("SELECT COUNT(*) FROM dapps WHERE token_symbol IS NOT NULL;")
    stats.append(['DApps with tokens', cur.fetchone()[0]])
    
    # Total TVL
    cur.execute("SELECT SUM(tvl) FROM dapps WHERE tvl > 0;")
    total_tvl = cur.fetchone()[0]
    if total_tvl:
        stats.append(['Total TVL', f"${total_tvl:,.0f}"])
    
    # Average TVL
    cur.execute("SELECT AVG(tvl) FROM dapps WHERE tvl > 0;")
    avg_tvl = cur.fetchone()[0]
    if avg_tvl:
        stats.append(['Average TVL', f"${avg_tvl:,.0f}"])
    
    # Total Market Cap
    cur.execute("SELECT SUM(market_cap) FROM dapps WHERE market_cap > 0;")
    total_market_cap = cur.fetchone()[0]
    if total_market_cap:
        stats.append(['Total Market Cap', f"${total_market_cap:,.0f}"])
    
    # Average Market Cap
    cur.execute("SELECT AVG(market_cap) FROM dapps WHERE market_cap > 0;")
    avg_market_cap = cur.fetchone()[0]
    if avg_market_cap:
        stats.append(['Average Market Cap', f"${avg_market_cap:,.0f}"])
    
    # Total Users
    cur.execute("SELECT SUM(users) FROM dapps WHERE users > 0;")
    total_users = cur.fetchone()[0]
    if total_users:
        stats.append(['Total Users', f"{total_users:,.0f}"])
    
    # Average Users
    cur.execute("SELECT AVG(users) FROM dapps WHERE users > 0;")
    avg_users = cur.fetchone()[0]
    if avg_users:
        stats.append(['Average Users', f"{avg_users:,.0f}"])
    
    headers = ['Statistic', 'Value']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(stats)
    
    cur.close()
    conn.close()
    
    print(f"✅ Exported {len(stats)} statistics to {output_file}")
    return len(stats)

def main():
    """Export all data to CSV files"""
    print("📤 Exporting DApp data to CSV files...")
    print("=" * 40)
    
    export_dir = f"exports"
    
    # Create export directory
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Export main DApp data
    dapp_count = export_dapps_to_csv(os.path.join(export_dir, "dapps.csv"))
    
    # Export pilot dataset
    pilot_count = export_pilot_dataset(os.path.join(export_dir, "pilot_dataset.csv"))
    
    # Export summary stats
    stats_count = export_summary_stats(os.path.join(export_dir, "summary_stats.csv"))
    
    print(f"\n🎉 Export complete!")
    print(f"📂 Files saved to: {export_dir}/")
    print(f"📊 Summary:")
    print(f"  • {dapp_count} DApps (full dataset)")
    print(f"  • {pilot_count} DApps (pilot dataset)")
    print(f"  • {stats_count} summary statistics")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "dapps":
            export_dapps_to_csv("dapps.csv")
        elif sys.argv[1] == "pilot":
            export_pilot_dataset("pilot_dataset.csv")
        elif sys.argv[1] == "stats":
            export_summary_stats("stats.csv")
        else:
            print("Usage: python export_csv.py [dapps|pilot|stats]")
    else:
        main() 