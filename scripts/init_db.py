import os
from configparser import ConfigParser

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
DB_NAME = _cfg["database"]["name"]
SUPERUSER = _cfg["database"]["user"]
PASSWORD = _cfg["database"]["password"]
HOST = _cfg["database"]["host"]
PORT = _cfg["database"]["port"]

def create_database():
    # Connect to default 'postgres' DB to issue CREATE DATABASE
    conn = psycopg2.connect(
        dbname=DB_NAME,
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
    # Connect to the newly created database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cur = conn.cursor()
    ddl = """
    -- Lookup tables
    CREATE TABLE IF NOT EXISTS category (
      category_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS industry (
      industry_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS chain (
      chain_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS l2_network (
      l2_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL,
      status VARCHAR(50),
      announced DATE
    );
    CREATE TABLE IF NOT EXISTS protocol (
      protocol_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS funding_source (
      fund_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS token_format (
      format_id SERIAL PRIMARY KEY,
      name VARCHAR(50) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS token (
      token_id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      symbol VARCHAR(50) NOT NULL,
      format_id INTEGER REFERENCES token_format(format_id)
    );
    CREATE TABLE IF NOT EXISTS fee_type (
      fee_type_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS governance_model (
      gov_model_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS metric_type (
      metric_type_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS activity_type (
      activity_id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL
    );

    -- Core DApp table
    CREATE TABLE IF NOT EXISTS dapp (
      dapp_id               SERIAL       PRIMARY KEY,
      name                  VARCHAR(255) NOT NULL,
      slug                  VARCHAR(255) NOT NULL UNIQUE,
      decentralisation_lvl  VARCHAR(50),
      multi_chain           BOOLEAN      DEFAULT FALSE,
      birth_date            DATE,
      status                VARCHAR(50),
      ownership_status      VARCHAR(100),
      capital_raised        NUMERIC      DEFAULT 0,
      showcase_fun          BOOLEAN      DEFAULT FALSE
    );
    ALTER TABLE dapp
      ADD COLUMN category_id  INTEGER REFERENCES category(category_id),
      ADD COLUMN industry_id  INTEGER REFERENCES industry(industry_id);

    -- M:N and 1:N relation tables
    CREATE TABLE IF NOT EXISTS dapp_chain (
      dapp_id  INTEGER REFERENCES dapp(dapp_id),
      chain_id INTEGER REFERENCES chain(chain_id),
      PRIMARY KEY (dapp_id, chain_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_l2 (
      dapp_id INTEGER REFERENCES dapp(dapp_id),
      l2_id   INTEGER REFERENCES l2_network(l2_id),
      PRIMARY KEY (dapp_id, l2_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_protocol (
      dapp_id     INTEGER REFERENCES dapp(dapp_id),
      protocol_id INTEGER REFERENCES protocol(protocol_id),
      role        VARCHAR(20),         -- e.g. 'Protocol A'
      PRIMARY KEY (dapp_id, protocol_id, role)
    );
    CREATE TABLE IF NOT EXISTS dapp_funding (
      dapp_id     INTEGER REFERENCES dapp(dapp_id),
      fund_id     INTEGER REFERENCES funding_source(fund_id),
      amount      NUMERIC,
      PRIMARY KEY (dapp_id, fund_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_token (
      dapp_id   INTEGER REFERENCES dapp(dapp_id),
      token_id  INTEGER REFERENCES token(token_id),
      PRIMARY KEY (dapp_id, token_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_fee (
      dapp_id        INTEGER REFERENCES dapp(dapp_id),
      fee_type_id    INTEGER REFERENCES fee_type(fee_type_id),
      rate           NUMERIC,
      charged_to     VARCHAR(100),
      recipient      VARCHAR(100),
      PRIMARY KEY (dapp_id, fee_type_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_governance (
      dapp_id      INTEGER REFERENCES dapp(dapp_id),
      gov_model_id INTEGER REFERENCES governance_model(gov_model_id),
      PRIMARY KEY (dapp_id, gov_model_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_metric (
      dapp_id        INTEGER REFERENCES dapp(dapp_id),
      metric_type_id INTEGER REFERENCES metric_type(metric_type_id),
      value          NUMERIC,
      PRIMARY KEY (dapp_id, metric_type_id)
    );
    CREATE TABLE IF NOT EXISTS dapp_activity (
      dapp_id     INTEGER REFERENCES dapp(dapp_id),
      activity_id INTEGER REFERENCES activity_type(activity_id),
      PRIMARY KEY (dapp_id, activity_id)
    );
    """
    cur.execute(ddl)
    conn.commit()
    print("→ Schema created/updated in", DB_NAME)
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_schema()
