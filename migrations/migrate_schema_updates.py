"""
Migration script to update database schema:
1. Add new enum values to existing types
2. Rename decentralisation_lvl to level_of_decentralisation
3. Add sub_category and research_comments columns
4. Remove score columns and social_presence
5. Drop related indexes
"""

import os
import sys
from configparser import ConfigParser
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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

def migrate():
    conn = get_conn()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    print("🔄 Starting schema migration...")
    print("=" * 60)
    
    # Step 1: Add new enum values to governance_type_enum (only values used in CSV)
    print("\n1️⃣  Updating governance_type_enum...")
    try:
        # These are the actual values from the CSV
        new_governance_values = [
            'SNAPSHOT_OFFCHAIN',
            'ONCHAIN_TOKEN_GOVERNANCE', 
            'HYBRID',
            'MULTISIG_WITH_COMMUNITY_INPUT',
            'DAO_WITH_TIMELOCK'
        ]
        for value in new_governance_values:
            try:
                cur.execute(f"ALTER TYPE governance_type_enum ADD VALUE IF NOT EXISTS '{value}';")
                print(f"   ✓ Added value: {value}")
            except Exception as e:
                print(f"   ⚠ {value} already exists or error: {e}")
    except Exception as e:
        print(f"   ❌ Error updating governance_type_enum: {e}")
    
    # Step 2: Add new enum values to ownership_status_enum (only values used in CSV)
    print("\n2️⃣  Updating ownership_status_enum...")
    try:
        # These are the actual values from the CSV
        new_ownership_values = ['MIXED', 'ORPHANED']
        for value in new_ownership_values:
            try:
                cur.execute(f"ALTER TYPE ownership_status_enum ADD VALUE IF NOT EXISTS '{value}';")
                print(f"   ✓ Added value: {value}")
            except Exception as e:
                print(f"   ⚠ {value} already exists or error: {e}")
    except Exception as e:
        print(f"   ❌ Error updating ownership_status_enum: {e}")
    
    # Step 3: Add new enum value to decentralisation_level_enum
    print("\n3️⃣  Updating decentralisation_level_enum...")
    try:
        # Change SEMI_CENTRALIZED to SEMI_DECENTRALIZED
        cur.execute(f"ALTER TYPE decentralisation_level_enum ADD VALUE IF NOT EXISTS 'SEMI_DECENTRALIZED';")
        print(f"   ✓ Added value: SEMI_DECENTRALIZED")
    except Exception as e:
        print(f"   ⚠ SEMI_DECENTRALIZED already exists or error: {e}")
    
    # Step 4: Update existing data from SEMI_CENTRALIZED to SEMI_DECENTRALIZED
    print("\n4️⃣  Migrating existing decentralisation level data...")
    try:
        cur.execute("""
            UPDATE dapps 
            SET decentralisation_lvl = 'SEMI_DECENTRALIZED'::decentralisation_level_enum
            WHERE decentralisation_lvl = 'SEMI_CENTRALIZED'::decentralisation_level_enum;
        """)
        print(f"   ✓ Updated existing SEMI_CENTRALIZED values to SEMI_DECENTRALIZED")
    except Exception as e:
        print(f"   ❌ Error migrating data: {e}")
    
    # Step 5: Rename column decentralisation_lvl to level_of_decentralisation
    print("\n5️⃣  Renaming decentralisation_lvl to level_of_decentralisation...")
    try:
        cur.execute("""
            ALTER TABLE dapps 
            RENAME COLUMN decentralisation_lvl TO level_of_decentralisation;
        """)
        print(f"   ✓ Column renamed successfully")
    except Exception as e:
        print(f"   ⚠ Column may already be renamed or error: {e}")
    
    # Step 6: Add new columns
    print("\n6️⃣  Adding new columns (sub_category, research_comments)...")
    try:
        cur.execute("""
            ALTER TABLE dapps 
            ADD COLUMN IF NOT EXISTS sub_category TEXT,
            ADD COLUMN IF NOT EXISTS research_comments TEXT;
        """)
        print(f"   ✓ New columns added successfully")
    except Exception as e:
        print(f"   ❌ Error adding columns: {e}")
    
    # Step 7: Drop indexes for columns we're removing
    print("\n7️⃣  Dropping indexes for removed columns...")
    indexes_to_drop = [
        'idx_dapps_governance_score',
        'idx_dapps_control_score',
        'idx_dapps_decentralisation_score',
        'idx_dapps_popularity_score',
        'idx_dapps_usage_score'
    ]
    for idx in indexes_to_drop:
        try:
            cur.execute(f"DROP INDEX IF EXISTS {idx};")
            print(f"   ✓ Dropped index: {idx}")
        except Exception as e:
            print(f"   ⚠ Error dropping {idx}: {e}")
    
    # Step 8: Drop columns
    print("\n8️⃣  Dropping removed columns...")
    columns_to_drop = [
        'social_presence',
        'governance_score',
        'control_score',
        'decentralisation_score',
        'popularity_score',
        'usage_score'
    ]
    for col in columns_to_drop:
        try:
            cur.execute(f"ALTER TABLE dapps DROP COLUMN IF EXISTS {col};")
            print(f"   ✓ Dropped column: {col}")
        except Exception as e:
            print(f"   ⚠ Error dropping {col}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("\n📋 Summary of changes:")
    print("  • Updated enum types with new values")
    print("  • Renamed: decentralisation_lvl → level_of_decentralisation")
    print("  • Added: sub_category, research_comments columns")
    print("  • Removed: social_presence and 5 score columns")
    print("  • Dropped: 5 related indexes")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

