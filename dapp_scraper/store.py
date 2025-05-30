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

def store_records(records):
    """
    Store records in the simplified database schema
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
            
            # Insert/Update main dapp record
            cur.execute(
                """
                INSERT INTO dapps (
                    name, slug, category_id, status, industry, description, website,
                    chains, multi_chain, birth_date, ownership_status, decentralisation_lvl,
                    capital_raised, showcase_fun, token_name, token_symbol, token_format,
                    governance_type, twitter, discord, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (slug) DO UPDATE SET
                    name = EXCLUDED.name,
                    category_id = EXCLUDED.category_id,
                    status = EXCLUDED.status,
                    industry = EXCLUDED.industry,
                    description = EXCLUDED.description,
                    website = EXCLUDED.website,
                    chains = EXCLUDED.chains,
                    multi_chain = EXCLUDED.multi_chain,
                    birth_date = EXCLUDED.birth_date,
                    ownership_status = EXCLUDED.ownership_status,
                    decentralisation_lvl = EXCLUDED.decentralisation_lvl,
                    capital_raised = EXCLUDED.capital_raised,
                    showcase_fun = EXCLUDED.showcase_fun,
                    token_name = EXCLUDED.token_name,
                    token_symbol = EXCLUDED.token_symbol,
                    token_format = EXCLUDED.token_format,
                    governance_type = EXCLUDED.governance_type,
                    twitter = EXCLUDED.twitter,
                    discord = EXCLUDED.discord,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (
                    rec["name"], rec["slug"], category_id, rec.get("status", "active"),
                    rec.get("industry"), rec.get("description"), rec.get("website"),
                    chains_str, rec.get("multi_chain", False), rec.get("birth_date"),
                    rec.get("ownership_status"), rec.get("decentralisation_lvl"),
                    rec.get("capital_raised", 0), rec.get("showcase_fun", False),
                    token_name, token_symbol, token_format, governance_type,
                    rec.get("twitter"), rec.get("discord"), datetime.now()
                )
            )
            
            # Get the dapp ID
            cur.execute("SELECT id FROM dapps WHERE slug = %s;", (rec["slug"],))
            dapp_id = cur.fetchone()[0]
            
            # Clear existing metrics for this dapp (for today)
            cur.execute(
                "DELETE FROM dapp_metrics WHERE dapp_id = %s AND metric_date = CURRENT_DATE;",
                (dapp_id,)
            )
            
            # Insert metrics
            for metric_name, metric_value in rec.get("metrics", {}).items():
                if metric_name and metric_value is not None:
                    try:
                        # Convert to float if possible
                        numeric_value = float(metric_value)
                        cur.execute(
                            """
                            INSERT INTO dapp_metrics (dapp_id, metric_name, metric_value, metric_date)
                            VALUES (%s, %s, %s, CURRENT_DATE)
                            ON CONFLICT (dapp_id, metric_name, metric_date)
                            DO UPDATE SET metric_value = EXCLUDED.metric_value;
                            """,
                            (dapp_id, metric_name, numeric_value)
                        )
                    except (ValueError, TypeError):
                        print(f"⚠️ Skipping metric {metric_name} with invalid value: {metric_value}")
            
            # Clear existing fees for this dapp
            cur.execute("DELETE FROM dapp_fees WHERE dapp_id = %s;", (dapp_id,))
            
            # Insert fees
            for fee_data in rec.get("fees", []):
                if fee_data.get("type"):
                    cur.execute(
                        """
                        INSERT INTO dapp_fees (dapp_id, fee_type, rate, charged_to, recipient)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (
                            dapp_id, fee_data["type"], fee_data.get("rate"),
                            fee_data.get("charged_to"), fee_data.get("recipient")
                        )
                    )
            
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

def get_recent_dapps(limit=10):
    """Get recently updated DApps"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name, slug, category, chains, updated_at
        FROM dapp_summary 
        ORDER BY updated_at DESC 
        LIMIT %s;
        """,
        (limit,)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results 