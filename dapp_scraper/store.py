import os
from configparser import ConfigParser
import psycopg2
from datetime import datetime

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

def get_or_create_category(cur, category_name):
    """Get or create category ID"""
    if not category_name or category_name.strip() == "":
        return None
        
    cur.execute(
        "INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (category_name,)
    )
    cur.execute("SELECT id FROM categories WHERE name = %s;", (category_name,))
    result = cur.fetchone()
    return result[0] if result else None

def get_or_create_industry(cur, industry_name):
    """Get or create industry ID"""
    if not industry_name or industry_name.strip() == "":
        return None
        
    cur.execute(
        "INSERT INTO industries (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (industry_name,)
    )
    cur.execute("SELECT id FROM industries WHERE name = %s;", (industry_name,))
    result = cur.fetchone()
    return result[0] if result else None

def store_records(records):
    """
    Store records in the extended database schema
    """
    conn = get_conn()
    cur = conn.cursor()

    for rec in records:
        try:
            print(f"Storing DApp: {rec['name']}")
            
            # Get category ID
            category_id = None
            if rec.get("category"):
                category_id = get_or_create_category(cur, rec["category"])
            
            # Get industry ID
            industry_id = None
            if rec.get("industry"):
                industry_id = get_or_create_industry(cur, rec["industry"])
            
            # Prepare chains as comma-separated string
            chains_str = ",".join(rec.get("chains", [])) if rec.get("chains") else ""
            
            # Get token info (first token if multiple)
            token_name = None
            token_symbol = None
            token_format = None
            if rec.get("tokens") and len(rec["tokens"]) > 0:
                first_token = rec["tokens"][0]
                token_name = first_token.get("name")
                token_symbol = first_token.get("symbol")
                token_format = first_token.get("format")
            
            # Get governance type (first one if multiple)
            governance_type = None
            if rec.get("governance") and len(rec["governance"]) > 0:
                governance_type = rec["governance"][0]
            
            # Extract metrics data
            metrics = rec.get("metrics", {})
            tvl = metrics.get("tvl", 0)
            users = metrics.get("users", 0)
            volume = metrics.get("volume", 0)
            transactions = metrics.get("transactions", 0)
            market_cap = metrics.get("market_cap", 0)
            
            # Extract market data (from coinmarketcap)
            market_data = rec.get("market_data", {})
            circulating_supply = market_data.get("circulating_supply", 0)
            total_supply = market_data.get("total_supply", 0)
            max_supply = market_data.get("max_supply", 0)
            
            # Extract USD quote data
            quote_usd = market_data.get("quote", {}).get("USD", {})
            price = quote_usd.get("price", 0)
            volume_24h = quote_usd.get("volume_24h", 0)
            volume_change_24h = quote_usd.get("volume_change_24h", 0)
            percent_change_1h = quote_usd.get("percent_change_1h", 0)
            percent_change_24h = quote_usd.get("percent_change_24h", 0)
            percent_change_7d = quote_usd.get("percent_change_7d", 0)
            percent_change_30d = quote_usd.get("percent_change_30d", 0)
            market_cap_dominance = quote_usd.get("market_cap_dominance", 0)
            fully_diluted_market_cap = quote_usd.get("fully_diluted_market_cap", 0)
            last_updated = quote_usd.get("last_updated")
            
            # Parse last_updated if it's a string
            if last_updated and isinstance(last_updated, str):
                try:
                    last_updated = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                except:
                    last_updated = None
            
            # Check if a record with the same name or slug already exists
            cur.execute(
                "SELECT id FROM dapps WHERE name = %s OR slug = %s;", 
                (rec["name"], rec["slug"])
            )
            existing_record = cur.fetchone()
            
            if existing_record:
                # Update existing record
                existing_id = existing_record[0]
                cur.execute(
                    """
                    UPDATE dapps SET
                        name = %s,
                        slug = %s,
                        category_id = %s,
                        status = %s,
                        industry_id = %s,
                        description = %s,
                        website = %s,
                        chains = %s,
                        multi_chain = %s,
                        birth_date = %s,
                        ownership_status = %s,
                        decentralisation_lvl = %s,
                        capital_raised = %s,
                        showcase_fun = %s,
                        token_name = %s,
                        token_symbol = %s,
                        token_format = %s,
                        governance_type = %s,
                        twitter = %s,
                        discord = %s,
                        tvl = %s,
                        users = %s,
                        volume = %s,
                        transactions = %s,
                        market_cap = %s,
                        circulating_supply = %s,
                        total_supply = %s,
                        max_supply = %s,
                        price = %s,
                        volume_24h = %s,
                        volume_change_24h = %s,
                        percent_change_1h = %s,
                        percent_change_24h = %s,
                        percent_change_7d = %s,
                        percent_change_30d = %s,
                        market_cap_dominance = %s,
                        fully_diluted_market_cap = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                    """,
                    (
                        rec["name"], rec["slug"], category_id, rec.get("status", "active"),
                        industry_id, rec.get("description"), rec.get("website"),
                        chains_str, rec.get("multi_chain", False), rec.get("birth_date"),
                        rec.get("ownership_status"), rec.get("decentralisation_lvl"),
                        rec.get("capital_raised", 0), rec.get("showcase_fun", False),
                        token_name, token_symbol, token_format, governance_type,
                        rec.get("twitter"), rec.get("discord"),
                        tvl, users, volume, transactions, market_cap,
                        circulating_supply, total_supply, max_supply,
                        price, volume_24h, volume_change_24h,
                        percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d,
                        market_cap_dominance, fully_diluted_market_cap,
                        existing_id
                    )
                )
                dapp_id = existing_id
            else:
                # Insert new record
                cur.execute(
                    """
                    INSERT INTO dapps (
                        name, slug, category_id, status, industry_id, description, website,
                        chains, multi_chain, birth_date, ownership_status, decentralisation_lvl,
                        capital_raised, showcase_fun, token_name, token_symbol, token_format,
                        governance_type, twitter, discord,
                        tvl, users, volume, transactions, market_cap,
                        circulating_supply, total_supply, max_supply,
                        price, volume_24h, volume_change_24h,
                        percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d,
                        market_cap_dominance, fully_diluted_market_cap
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id;
                    """,
                    (
                        rec["name"], rec["slug"], category_id, rec.get("status", "active"),
                        industry_id, rec.get("description"), rec.get("website"),
                        chains_str, rec.get("multi_chain", False), rec.get("birth_date"),
                        rec.get("ownership_status"), rec.get("decentralisation_lvl"),
                        rec.get("capital_raised", 0), rec.get("showcase_fun", False),
                        token_name, token_symbol, token_format, governance_type,
                        rec.get("twitter"), rec.get("discord"),
                        tvl, users, volume, transactions, market_cap,
                        circulating_supply, total_supply, max_supply,
                        price, volume_24h, volume_change_24h,
                        percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d,
                        market_cap_dominance, fully_diluted_market_cap
                    )
                )
                dapp_id = cur.fetchone()[0]
            
            print(f"✅ Successfully stored DApp: {rec['name']}")
            
        except Exception as e:
            print(f"❌ Error storing DApp {rec.get('name', 'Unknown')}: {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()

def store_single_record(record):
    """Store a single record - wrapper for store_records"""
    store_records([record])

def get_dapp_count():
    """Get total number of DApps"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dapps;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def get_recent_dapps(limit):
    """Get recently updated DApps"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT d.name, d.slug, c.name as category, d.chains, d.updated_at
        FROM dapps d
        LEFT JOIN categories c ON d.category_id = c.id
        ORDER BY d.updated_at DESC 
        LIMIT %s;
        """,
        (limit,)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results 