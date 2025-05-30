import os
from configparser import ConfigParser
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
DB_NAME = _cfg["database"]["name"]
SUPERUSER = _cfg["database"]["user"]
PASSWORD = _cfg["database"]["password"]
HOST = _cfg["database"]["host"]
PORT = _cfg["database"]["port"]

def create_database():
    # Connect to default 'postgres' DB to issue CREATE DATABASE
    conn = psycopg2.connect(
        dbname="postgres",
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    # only create if not exists
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"→ Database '{DB_NAME}' created.")
    else:
        print(f"→ Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()

def drop_existing_tables():
    """Drop existing complex tables"""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cur = conn.cursor()
    
    # Drop all existing tables
    tables_to_drop = [
        'dapp_activity', 'dapp_metric', 'dapp_governance', 'dapp_fee', 
        'dapp_token', 'dapp_funding', 'dapp_protocol', 'dapp_l2', 
        'dapp_chain', 'activity_type', 'metric_type', 'governance_model', 
        'fee_type', 'token', 'token_format', 'funding_source', 'protocol', 
        'l2_network', 'chain', 'industry', 'category', 'dapp'
    ]
    
    for table in tables_to_drop:
        try:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"✅ Dropped table: {table}")
        except Exception as e:
            print(f"⚠️ Could not drop {table}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()

def create_simple_schema():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cur = conn.cursor()
    ddl = """
    -- Simple lookup table for categories
    CREATE TABLE IF NOT EXISTS categories (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );

    -- Main DApp table with most data flattened
    CREATE TABLE IF NOT EXISTS dapps (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      slug VARCHAR(255) UNIQUE NOT NULL,
      category_id INTEGER REFERENCES categories(id),
      
      -- Basic info
      status VARCHAR(50) DEFAULT 'active',
      industry VARCHAR(100),
      description TEXT,
      website VARCHAR(500),
      
      -- Blockchain info (simplified - store as comma-separated for multi-chain)
      chains TEXT,  -- e.g., "Ethereum,Polygon,BSC"
      multi_chain BOOLEAN DEFAULT FALSE,
      
      -- Dates and ownership
      birth_date DATE,
      ownership_status VARCHAR(100),
      decentralisation_lvl VARCHAR(50),
      
      -- Financial data
      capital_raised NUMERIC DEFAULT 0,
      showcase_fun BOOLEAN DEFAULT FALSE,
      
      -- Tokens (simplified - store main token info)
      token_name VARCHAR(100),
      token_symbol VARCHAR(20),
      token_format VARCHAR(50),
      
      -- Governance (simplified)
      governance_type VARCHAR(100),  -- e.g., "DAO", "Centralized", "Multi-sig"
      
      -- Social & Links
      twitter VARCHAR(200),
      discord VARCHAR(200),
      
      -- Timestamps
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Metrics table for key-value metrics
    CREATE TABLE IF NOT EXISTS dapp_metrics (
      id SERIAL PRIMARY KEY,
      dapp_id INTEGER REFERENCES dapps(id) ON DELETE CASCADE,
      metric_name VARCHAR(100) NOT NULL,
      metric_value NUMERIC,
      metric_date DATE DEFAULT CURRENT_DATE,
      UNIQUE(dapp_id, metric_name, metric_date)
    );

    -- Simplified fees table
    CREATE TABLE IF NOT EXISTS dapp_fees (
      id SERIAL PRIMARY KEY,
      dapp_id INTEGER REFERENCES dapps(id) ON DELETE CASCADE,
      fee_type VARCHAR(100) NOT NULL,
      rate NUMERIC,
      charged_to VARCHAR(100),
      recipient VARCHAR(100)
    );

    -- Insert some default categories
    INSERT INTO categories (name) VALUES 
      ('DeFi'), ('Gaming'), ('Marketplaces'), ('Social'), ('Wallets'), 
      ('Infrastructure'), ('DAO'), ('NFT'), ('Yield Farming'), ('DEX'),
      ('Lending'), ('Insurance'), ('Analytics'), ('Bridge'), ('Staking')
    ON CONFLICT (name) DO NOTHING;

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_dapps_category ON dapps(category_id);
    CREATE INDEX IF NOT EXISTS idx_dapps_chains ON dapps USING gin(to_tsvector('english', chains));
    CREATE INDEX IF NOT EXISTS idx_dapps_industry ON dapps(industry);
    CREATE INDEX IF NOT EXISTS idx_metrics_dapp ON dapp_metrics(dapp_id);
    CREATE INDEX IF NOT EXISTS idx_metrics_name ON dapp_metrics(metric_name);
    CREATE INDEX IF NOT EXISTS idx_fees_dapp ON dapp_fees(dapp_id);

    -- Create view for easy querying
    CREATE OR REPLACE VIEW dapp_summary AS
    SELECT 
      d.id,
      d.name,
      d.slug,
      c.name as category,
      d.industry,
      d.chains,
      d.multi_chain,
      d.status,
      d.ownership_status,
      d.decentralisation_lvl,
      d.token_symbol,
      d.governance_type,
      d.birth_date,
      d.capital_raised,
      d.website,
      -- Get key metrics in columns
      (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'tvl' ORDER BY metric_date DESC LIMIT 1) as tvl,
      (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'users' ORDER BY metric_date DESC LIMIT 1) as users,
      (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'volume' ORDER BY metric_date DESC LIMIT 1) as volume,
      (SELECT metric_value FROM dapp_metrics WHERE dapp_id = d.id AND metric_name = 'transactions' ORDER BY metric_date DESC LIMIT 1) as transactions
    FROM dapps d
    LEFT JOIN categories c ON d.category_id = c.id;
    """
    cur.execute(ddl)
    conn.commit()
    print("→ Simplified schema created in", DB_NAME)
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("🗃️ Creating Simplified Database Schema")
    print("=" * 40)
    
    create_database()
    
    choice = input("⚠️ This will DROP all existing tables and create new simplified ones. Continue? (y/N): ")
    if choice.lower() == 'y':
        drop_existing_tables()
        create_simple_schema()
        print("\n✅ Simplified database schema created!")
        print("📋 Tables created:")
        print("  • categories - DApp categories")
        print("  • dapps - Main DApp information (flattened)")
        print("  • dapp_metrics - Key-value metrics")
        print("  • dapp_fees - Fee information")
        print("  • dapp_summary - Easy query view")
    else:
        print("❌ Operation cancelled.") 