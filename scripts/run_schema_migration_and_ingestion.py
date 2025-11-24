"""
Convenience script to run schema migration and data ingestion in sequence.
This ensures the database schema is updated before attempting to ingest new data.
"""

import os
import sys
import subprocess

def run_command(script_path, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Define paths
    migration_script = os.path.join(project_root, 'migrations', 'migrate_schema_updates.py')
    ingestion_script = os.path.join(script_dir, 'ingest_pilot_data.py')
    csv_file = '/Users/kristian.kirilov/Downloads/pilot_dataset - pilot_dataset (1).csv'
    
    print("🎯 Schema Migration and Data Ingestion Pipeline")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Migration script: {migration_script}")
    print(f"Ingestion script: {ingestion_script}")
    print(f"CSV file: {csv_file}")
    
    # Step 1: Run migration
    if not run_command(migration_script, "Schema Migration"):
        print("\n⚠️  Migration failed. Stopping pipeline.")
        return 1
    
    # Step 2: Run ingestion with CSV file
    if os.path.exists(csv_file):
        print(f"\n{'='*60}")
        print(f"🚀 Data Ingestion from CSV")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run(
                [sys.executable, ingestion_script, csv_file],
                check=True,
                capture_output=False,
                text=True
            )
            print(f"✅ Data Ingestion completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Data Ingestion failed with exit code {e.returncode}")
            return 1
        except Exception as e:
            print(f"❌ Error running Data Ingestion: {e}")
            return 1
    else:
        print(f"\n⚠️  CSV file not found: {csv_file}")
        print("Please specify the correct path to your CSV file.")
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline completed successfully!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("  ✓ Database schema updated")
    print("  ✓ Data ingested from CSV")
    print("\nYour database is now ready with the updated schema and enriched data!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

