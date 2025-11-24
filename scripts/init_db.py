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

def create_schema():
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
    -- Create ENUM types for standardized values
    DO $$ BEGIN
        CREATE TYPE ownership_status_enum AS ENUM (
            'COMPANY_OWNED',
            'FOUNDATION_OWNED', 
            'DAO_OWNED',
            'MULTISIG_COUNCIL',
            'HYBRID',
            'ORPHANED_IMMUTABLE',
            'UNKNOWN'
        );
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    DO $$ BEGIN
        CREATE TYPE governance_type_enum AS ENUM (
            'NONE',
            'TEAM_CONTROLLED',
            'COMMUNITY_MULTISIG',
            'OFFCHAIN_TOKEN_VOTING',
            'ONCHAIN_GOVERNANCE',
            'ONCHAIN_GOV_WITH_TIMELOCK'
        );
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    DO $$ BEGIN
        CREATE TYPE decentralisation_level_enum AS ENUM (
            'CENTRALIZED',
            'SEMI_CENTRALIZED',
            'DECENTRALIZED'
        );
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    -- Categories lookup table
    CREATE TABLE IF NOT EXISTS categories (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );

    -- Main DApp table with extended columns
    CREATE TABLE IF NOT EXISTS dapps (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      slug VARCHAR(255) UNIQUE NOT NULL,
      category_id INTEGER REFERENCES categories(id),
      gecko_id VARCHAR(100),
      cmc_id VARCHAR(100),
      
      -- Basic info
      is_active BOOLEAN DEFAULT TRUE,
      description TEXT,
      website VARCHAR(500),
      tags TEXT,  -- Combined tags from DappRadar and CoinMarketCap
      sub_category TEXT,  -- Sub-category for more granular classification
      
      -- Blockchain info
      chains TEXT,  -- e.g., "Ethereum,Polygon,BSC"
      multi_chain BOOLEAN DEFAULT FALSE,
      
      -- Dates and ownership
      birth_date DATE,
      
      -- Financial data
      capital_raised NUMERIC DEFAULT 0,
      
      -- Tokens
      token_name VARCHAR(100),
      token_symbol VARCHAR(20),
      token_format VARCHAR(50),
      
      -- External IDs
      gecko_id VARCHAR(100),
      cmc_id VARCHAR(20),
      
      -- Governance and Decentralization
      governance_type governance_type_enum,
      ownership_status ownership_status_enum,
      level_of_decentralisation decentralisation_level_enum,
      research_comments TEXT  -- Research notes and comments
      
      -- DApp Metrics
      tvl NUMERIC DEFAULT 0,
      tvl_ratio NUMERIC DEFAULT 0,
      users BIGINT DEFAULT 0,
      volume NUMERIC DEFAULT 0,
      transactions BIGINT DEFAULT 0,
      market_cap NUMERIC DEFAULT 0,
      mcap NUMERIC DEFAULT 0,
      circulating_supply NUMERIC DEFAULT 0,
      total_supply NUMERIC DEFAULT 0,
      max_supply NUMERIC DEFAULT 0,
      
      -- Price and Market Data
      price NUMERIC DEFAULT 0,
      volume_24h NUMERIC DEFAULT 0,
      volume_change_24h NUMERIC DEFAULT 0,
      percent_change_1h NUMERIC DEFAULT 0,
      percent_change_24h NUMERIC DEFAULT 0,
      percent_change_7d NUMERIC DEFAULT 0,
      percent_change_30d NUMERIC DEFAULT 0,
      percent_change_60d NUMERIC DEFAULT 0,
      percent_change_90d NUMERIC DEFAULT 0,
      cmc_rank INTEGER DEFAULT 0,
      market_cap_dominance NUMERIC DEFAULT 0,
      fully_diluted_market_cap NUMERIC DEFAULT 0,
      
      -- Timestamps
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- TVL Historical Data table (from DeFiLlama)
    CREATE TABLE IF NOT EXISTS tvl_historical (
      id SERIAL PRIMARY KEY,
      dapp_id INTEGER REFERENCES dapps(id) ON DELETE CASCADE,
      date DATE NOT NULL,
      total_liquidity_usd NUMERIC NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Raises/Funding Data table (from DeFiLlama)  
    CREATE TABLE IF NOT EXISTS raises (
      id SERIAL PRIMARY KEY,
      dapp_id INTEGER REFERENCES dapps(id) ON DELETE CASCADE,
      date DATE NOT NULL,
      name VARCHAR(255),
      round VARCHAR(100),
      amount NUMERIC,
      chains TEXT,
      sector TEXT,
      category VARCHAR(100),
      category_group VARCHAR(100),
      source VARCHAR(500),
      lead_investors TEXT,
      other_investors TEXT,
      valuation NUMERIC,
      defillama_id VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_dapps_category ON dapps(category_id);
    CREATE INDEX IF NOT EXISTS idx_dapps_chains ON dapps USING gin(to_tsvector('english', chains));
    CREATE INDEX IF NOT EXISTS idx_dapps_tvl ON dapps(tvl);
    CREATE INDEX IF NOT EXISTS idx_dapps_users ON dapps(users);
    CREATE INDEX IF NOT EXISTS idx_dapps_volume ON dapps(volume);
    CREATE INDEX IF NOT EXISTS idx_dapps_market_cap ON dapps(market_cap);
    CREATE INDEX IF NOT EXISTS idx_dapps_is_active ON dapps(is_active);
    CREATE INDEX IF NOT EXISTS idx_dapps_tags ON dapps USING gin(to_tsvector('english', tags));
    CREATE INDEX IF NOT EXISTS idx_dapps_governance_type ON dapps(governance_type);
    CREATE INDEX IF NOT EXISTS idx_dapps_ownership_status ON dapps(ownership_status);
    CREATE INDEX IF NOT EXISTS idx_dapps_level_of_decentralisation ON dapps(level_of_decentralisation);
    
    -- Indexes for new tables
    CREATE INDEX IF NOT EXISTS idx_tvl_historical_dapp_id ON tvl_historical(dapp_id);
    CREATE INDEX IF NOT EXISTS idx_tvl_historical_date ON tvl_historical(date);
    CREATE INDEX IF NOT EXISTS idx_raises_dapp_id ON raises(dapp_id);
    CREATE INDEX IF NOT EXISTS idx_raises_date ON raises(date);
    """
    cur.execute(ddl)
    conn.commit()
    print("→ Extended schema created in", DB_NAME)
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("🗃️ Creating Extended Database Schema")
    print("=" * 40)
    
    create_database()
    create_schema()
    print("\n✅ Extended database schema created!")
    print("📋 Tables created:")
    print("  • categories - DApp categories lookup")
    print("  • dapps - Extended DApp information with governance & metrics")
    print("  • tvl_historical - Historical TVL data from DeFiLlama")
    print("  • raises - Funding/raises data from DeFiLlama")
    print("\n📝 Schema includes:")
    print("  • Governance tracking (type, ownership, decentralisation)")
    print("  • Sub-category and research comments")
    print("  • Token information and metrics") 