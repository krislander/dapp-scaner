#!/usr/bin/env python3
"""
Migration script to add new columns to existing database
Adds: gecko_id, cmc_id, mcap columns
"""

import os
from configparser import ConfigParser
import psycopg2

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

def check_column_exists(cur, table_name, column_name):
    """Check if a column exists in a table"""
    cur.execute("""
        SELECT COUNT(*) 
        FROM information_schema.columns 
        WHERE table_name = %s AND column_name = %s
    """, (table_name, column_name))
    return cur.fetchone()[0] > 0

def add_new_columns():
    """Add new columns to the dapps table"""
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        print("🔧 Adding new columns to dapps table...")
        
        # List of columns to add
        columns_to_add = [
            ("gecko_id", "VARCHAR(100)"),
            ("cmc_id", "VARCHAR(20)"),
            ("mcap", "NUMERIC DEFAULT 0")
        ]
        
        for column_name, column_def in columns_to_add:
            if not check_column_exists(cur, "dapps", column_name):
                print(f"  ➕ Adding column: {column_name}")
                cur.execute(f"ALTER TABLE dapps ADD COLUMN {column_name} {column_def};")
                print(f"  ✅ Column {column_name} added successfully")
            else:
                print(f"  ⚠️ Column {column_name} already exists, skipping")
        
        # Add indexes for the new columns
        print("\n🔧 Adding indexes for new columns...")
        
        indexes_to_add = [
            ("idx_dapps_gecko_id", "gecko_id"),
            ("idx_dapps_cmc_id", "cmc_id"),
            ("idx_dapps_mcap", "mcap")
        ]
        
        for index_name, column_name in indexes_to_add:
            try:
                cur.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON dapps({column_name});")
                print(f"  ✅ Index {index_name} created")
            except psycopg2.Error as e:
                print(f"  ⚠️ Index {index_name} may already exist: {e}")
        
        conn.commit()
        print("\n🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def verify_columns():
    """Verify that all required columns exist"""
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        print("\n🔍 Verifying column structure...")
        
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'dapps' 
            ORDER BY ordinal_position
        """)
        
        columns = cur.fetchall()
        column_names = [col[0] for col in columns]
        
        required_new_columns = ['gecko_id', 'cmc_id', 'mcap']
        missing_columns = [col for col in required_new_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        else:
            print("✅ All required columns present")
            print(f"📊 Total columns in dapps table: {len(columns)}")
            
            # Show the new columns
            for col_name, col_type in columns:
                if col_name in required_new_columns:
                    print(f"  • {col_name}: {col_type}")
            
            return True
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("🗃️ Database Migration: Adding New Columns")
    print("=" * 50)
    
    try:
        add_new_columns()
        
        if verify_columns():
            print("\n✅ Migration successful! New columns are ready to use.")
        else:
            print("\n❌ Migration verification failed!")
            
    except Exception as e:
        print(f"\n💥 Migration crashed: {e}")
        print("Please check your database connection and try again.") 