import os
from configparser import ConfigParser
import psycopg2
from psycopg2.extras import execute_values

_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini'))
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

def get_or_create(cur, table, name_col, value):
    """
    INSERT INTO table(name_col) VALUES (%s)
      ON CONFLICT DO NOTHING;
    SELECT id_col FROM table WHERE name_col = %s;
    Returns the id.
    Assumes PK is table_id or name table_id: e.g. category -> category_id.
    """
    id_col = table + "_id"
    cur.execute(
        f"INSERT INTO {table}({name_col}) VALUES (%s) ON CONFLICT ({name_col}) DO NOTHING;",
        (value,)
    )
    cur.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = %s;",
        (value,)
    )
    return cur.fetchone()[0]

def store_records(records):
    """
    For each normalized record, upsert into:
      - category
      - dapp
      - chain
      - dapp_chain
      - metric_type
      - dapp_metric
    """
    conn = get_conn()
    cur  = conn.cursor()

    for rec in records:
        # 1. category
        cat_id = None
        if rec.get("category"):
            cat_id = get_or_create(cur, "category", "name", rec["category"])

        # 2. insert dapp
        #    ON CONFLICT(slug) DO NOTHING
        cur.execute(
            """
            INSERT INTO dapp(name, slug, multi_chain, category_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (slug) DO NOTHING;
            """,
            (rec["name"], rec["slug"], len(rec["chains"]) > 1, cat_id)
        )
        # retrieve dapp_id
        cur.execute("SELECT dapp_id FROM dapp WHERE slug = %s;", (rec["slug"],))
        dapp_id = cur.fetchone()[0]

        # 3. chains & dapp_chain
        for ch in rec.get("chains", []):
            chain_id = get_or_create(cur, "chain", "name", ch)
            cur.execute(
                """
                INSERT INTO dapp_chain(dapp_id, chain_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (dapp_id, chain_id)
            )

        # 4. metrics & dapp_metric
        for m_name, m_val in rec.get("metrics", {}).items():
            metric_id = get_or_create(cur, "metric_type", "name", m_name)
            cur.execute(
                """
                INSERT INTO dapp_metric(dapp_id, metric_type_id, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (dapp_id, metric_type_id)
                  DO UPDATE SET value = EXCLUDED.value;
                """,
                (dapp_id, metric_id, m_val)
            )

    conn.commit()
    cur.close()
    conn.close()
