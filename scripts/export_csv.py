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

def export_metrics_to_csv(output_file="dapp_metrics_export.csv"):
    """Export all metrics to a separate CSV file"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    query = """
    SELECT 
        d.name as dapp_name,
        d.slug,
        c.name as category,
        dm.metric_name,
        dm.metric_value,
        dm.metric_date
    FROM dapp_metrics dm
    JOIN dapps d ON dm.dapp_id = d.id
    LEFT JOIN categories c ON d.category_id = c.id
    ORDER BY d.name, dm.metric_name, dm.metric_date DESC;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    
    headers = ['dapp_name', 'slug', 'category', 'metric_name', 'metric_value', 'metric_date']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    
    cur.close()
    conn.close()
    
    print(f"✅ Exported {len(rows)} metrics to {output_file}")
    return len(rows)

def export_fees_to_csv(output_file="dapp_fees_export.csv"):
    """Export all fees to a CSV file"""
    
    conn = get_conn()
    cur = conn.cursor()
    
    query = """
    SELECT 
        d.name as dapp_name,
        d.slug,
        c.name as category,
        df.fee_type,
        df.rate,
        df.charged_to,
        df.recipient
    FROM dapp_fees df
    JOIN dapps d ON df.dapp_id = d.id
    LEFT JOIN categories c ON d.category_id = c.id
    ORDER BY d.name, df.fee_type;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    
    headers = ['dapp_name', 'slug', 'category', 'fee_type', 'rate', 'charged_to', 'recipient']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    
    cur.close()
    conn.close()
    
    print(f"✅ Exported {len(rows)} fees to {output_file}")
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
    
    # Export metrics
    metrics_count = export_metrics_to_csv(os.path.join(export_dir, "metrics.csv"))
    
    # Export fees
    fees_count = export_fees_to_csv(os.path.join(export_dir, "fees.csv"))
    
    # Export summary stats
    stats_count = export_summary_stats(os.path.join(export_dir, "summary_stats.csv"))
    
    print(f"\n🎉 Export complete!")
    print(f"📂 Files saved to: {export_dir}/")
    print(f"📊 Summary:")
    print(f"  • {dapp_count} DApps")
    print(f"  • {metrics_count} metrics entries")
    print(f"  • {fees_count} fee entries")
    print(f"  • {stats_count} summary statistics")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "dapps":
            export_dapps_to_csv("dapps.csv")
        elif sys.argv[1] == "metrics":
            export_metrics_to_csv("metrics.csv")
        elif sys.argv[1] == "fees":
            export_fees_to_csv("fees.csv")
        elif sys.argv[1] == "stats":
            export_summary_stats("stats.csv")
        else:
            print("Usage: python export_simple_csv.py [dapps|metrics|fees|stats]")
    else:
        main() 