import sys
import os
import csv
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dapp_scraper.store import get_conn

def export_dapps_to_csv(output_file="dapps_export.csv"):
    """Export all DApps to a single CSV file"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Query to get all DApp data with metrics in one row
    query = """
    SELECT 
        d.id,
        d.name,
        d.slug,
        c.name as category,
        d.industry,
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
        -- Get key metrics
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'tvl' ORDER BY metric_date DESC LIMIT 1) as tvl,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'users' ORDER BY metric_date DESC LIMIT 1) as users,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'volume' ORDER BY metric_date DESC LIMIT 1) as volume,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'transactions' ORDER BY metric_date DESC LIMIT 1) as transactions,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'balance' ORDER BY metric_date DESC LIMIT 1) as balance,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'change_1d' ORDER BY metric_date DESC LIMIT 1) as change_1d,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'change_7d' ORDER BY metric_date DESC LIMIT 1) as change_7d,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'mcap' ORDER BY metric_date DESC LIMIT 1) as market_cap,
        -- Get fees as concatenated string
        (SELECT string_agg(fee_type || ':' || COALESCE(rate::text, 'N/A'), '; ') FROM dapp_fees WHERE dapp_id = d.id) as fees
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
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
        'tvl', 'users', 'volume', 'transactions', 'balance', 'change_1d', 'change_7d',
        'market_cap', 'fees'
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
        d.industry,
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
        -- Get key metrics
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'tvl' ORDER BY metric_date DESC LIMIT 1) as tvl,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'users' ORDER BY metric_date DESC LIMIT 1) as users,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'volume' ORDER BY metric_date DESC LIMIT 1) as volume,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'transactions' ORDER BY metric_date DESC LIMIT 1) as transactions,
        (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'balance' ORDER BY metric_date DESC LIMIT 1) as balance,
        -- Get fees as concatenated string
        (SELECT string_agg(fee_type || ':' || COALESCE(rate::text, 'N/A'), '; ') FROM dapp_fees WHERE dapp_id = d.id) as fees,
        -- Count non-null fields for ordering (prioritize complete records)
        (
            CASE WHEN d.name IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN d.industry IS NOT NULL THEN 1 ELSE 0 END +
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
            CASE WHEN (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'users' ORDER BY metric_date DESC LIMIT 1) IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'volume' ORDER BY metric_date DESC LIMIT 1) IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'transactions' ORDER BY metric_date DESC LIMIT 1) IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'balance' ORDER BY metric_date DESC LIMIT 1) IS NOT NULL THEN 1 ELSE 0 END
        ) as completeness_score
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id
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
        'tvl', 'users', 'volume', 'transactions', 'balance', 'fees', 'completeness_score'
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
    cur.execute("SELECT SUM(metric_value) FROM dapp_metrics WHERE metric_name = 'tvl';")
    total_tvl = cur.fetchone()[0]
    if total_tvl:
        stats.append(['Total TVL', f"${total_tvl:,.0f}"])
    
    # Average TVL
    cur.execute("SELECT AVG(metric_value) FROM dapp_metrics WHERE metric_name = 'tvl' AND metric_value > 0;")
    avg_tvl = cur.fetchone()[0]
    if avg_tvl:
        stats.append(['Average TVL', f"${avg_tvl:,.0f}"])
    
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