"""
Script to ingest data from the manually enriched pilot dataset CSV into the database.
Updates existing dapps with new column values:
- sub_category
- governance_type
- ownership_status
- level_of_decentralisation
- research_comments
- token_symbol (updates)
- token_format (updates)
"""

import os
import sys
import csv
from configparser import ConfigParser
import psycopg2
from psycopg2.extras import execute_values

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

def clean_value(value):
    """Clean and normalize CSV values"""
    if value is None or value == '' or value.lower() == 'null':
        return None
    return value.strip()

def ingest_pilot_data(csv_file):
    """Ingest data from pilot dataset CSV"""
    
    print("📥 Ingesting pilot dataset...")
    print("=" * 60)
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"📄 Read {len(rows)} rows from CSV")
    
    # Track statistics
    stats = {
        'total': len(rows),
        'updated': 0,
        'not_found': 0,
        'errors': 0,
        'skipped': 0
    }
    
    not_found_dapps = []
    error_dapps = []
    
    for idx, row in enumerate(rows, 1):
        dapp_name = clean_value(row['name'])
        
        if not dapp_name:
            stats['skipped'] += 1
            continue
        
        try:
            # Check if dapp exists
            cur.execute("SELECT id FROM dapps WHERE name = %s", (dapp_name,))
            result = cur.fetchone()
            
            if not result:
                not_found_dapps.append(dapp_name)
                stats['not_found'] += 1
                continue
            
            dapp_id = result[0]
            
            # Prepare update data
            dapp_category = clean_value(row.get('dapp_category'))
            sub_category = clean_value(row.get('sub_category'))
            governance_type = clean_value(row.get('governance_type'))
            ownership_status = clean_value(row.get('ownership_status'))
            level_of_decentralisation = clean_value(row.get('level_of_decentralisation'))
            research_comments = clean_value(row.get('research comments'))
            token_symbol = clean_value(row.get('token_symbol'))
            token_format = clean_value(row.get('token_format'))
            
            # Build update query dynamically based on available data
            update_parts = []
            update_values = []
            
            if dapp_category is not None:
                update_parts.append("category_id = %s")
                update_values.append(dapp_category)

            if sub_category is not None:
                update_parts.append("sub_category = %s")
                update_values.append(sub_category)
            
            if governance_type is not None:
                update_parts.append("governance_type = %s::governance_type_enum")
                update_values.append(governance_type)
            
            if ownership_status is not None:
                update_parts.append("ownership_status = %s::ownership_status_enum")
                update_values.append(ownership_status)
            
            if level_of_decentralisation is not None:
                update_parts.append("level_of_decentralisation = %s::decentralisation_level_enum")
                update_values.append(level_of_decentralisation)
            
            if research_comments is not None:
                update_parts.append("research_comments = %s")
                update_values.append(research_comments)
            
            if token_symbol is not None:
                update_parts.append("token_symbol = %s")
                update_values.append(token_symbol)
            
            if token_format is not None:
                update_parts.append("token_format = %s")
                update_values.append(token_format)
            
            # Add updated_at timestamp
            update_parts.append("updated_at = CURRENT_TIMESTAMP")
            
            if update_parts:
                update_query = f"""
                    UPDATE dapps 
                    SET {', '.join(update_parts)}
                    WHERE id = %s
                """
                update_values.append(dapp_id)
                
                cur.execute(update_query, update_values)
                stats['updated'] += 1
                
                if idx % 50 == 0:
                    print(f"   ⏳ Processed {idx}/{len(rows)} rows...")
                    conn.commit()
            
        except Exception as e:
            stats['errors'] += 1
            error_dapps.append((dapp_name, str(e)))
            print(f"   ❌ Error processing {dapp_name}: {e}")
    
    # Commit final changes
    conn.commit()
    
    print("\n" + "=" * 60)
    print("✅ Ingestion completed!")
    print("\n📊 Statistics:")
    print(f"  • Total rows in CSV: {stats['total']}")
    print(f"  • Successfully updated: {stats['updated']}")
    print(f"  • Not found in DB: {stats['not_found']}")
    print(f"  • Errors: {stats['errors']}")
    print(f"  • Skipped (no name): {stats['skipped']}")
    
    if not_found_dapps and len(not_found_dapps) <= 20:
        print(f"\n⚠️  DApps not found in database:")
        for dapp in not_found_dapps[:20]:
            print(f"    - {dapp}")
        if len(not_found_dapps) > 20:
            print(f"    ... and {len(not_found_dapps) - 20} more")
    
    if error_dapps and len(error_dapps) <= 10:
        print(f"\n❌ DApps with errors:")
        for dapp, error in error_dapps[:10]:
            print(f"    - {dapp}: {error}")
        if len(error_dapps) > 10:
            print(f"    ... and {len(error_dapps) - 10} more")
    
    cur.close()
    conn.close()
    
    return stats

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Ingest pilot dataset into database')
    parser.add_argument(
        'csv_file',
        nargs='?',
        default='/Users/kristian.kirilov/Downloads/pilot_dataset - pilot_dataset (1).csv',
        help='Path to the pilot dataset CSV file'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_file):
        print(f"❌ Error: CSV file not found: {args.csv_file}")
        sys.exit(1)
    
    try:
        ingest_pilot_data(args.csv_file)
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

