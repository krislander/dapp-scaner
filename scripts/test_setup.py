#!/usr/bin/env python3
"""
Test script to verify the DApp scraper setup
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import psycopg2
from configparser import ConfigParser

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        # Load configuration
        _cfg = ConfigParser()
        _cfg.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
        
        DB_NAME = _cfg["database"]["name"]
        USER = _cfg["database"]["user"]
        PASSWORD = _cfg["database"]["password"]
        HOST = _cfg["database"]["host"]
        PORT = _cfg["database"]["port"]
        
        # Test connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Database connection successful!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Test if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"📋 Found {len(tables)} tables:")
            for table in tables[:10]:  # Show first 10 tables
                print(f"   • {table[0]}")
            if len(tables) > 10:
                print(f"   ... and {len(tables) - 10} more")
        else:
            print("⚠️ No tables found. Run 'python scripts/init_db.py' first.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_api_configuration():
    """Test API configuration"""
    print("\n🔍 Testing API configuration...")
    
    try:
        _cfg = ConfigParser()
        _cfg.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
        
        # Test DappRadar config
        if _cfg.has_section('dappradar'):
            api_key = _cfg["dappradar"]["api_key"]
            if api_key and api_key != "your_dappradar_api_key":
                print("✅ DappRadar API key configured")
            else:
                print("⚠️ DappRadar API key not configured")
        
        # Test DeFiLlama config
        if _cfg.has_section('defillama'):
            print("✅ DeFiLlama configuration found")
        
        # Test CMC config
        if _cfg.has_section('coinmarketcap'):
            print("✅ CMC configuration found")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing imports...")
    
    try:
        import requests
        print("✅ requests")
        
        import psycopg2
        print("✅ psycopg2")
        
        import pandas
        print("✅ pandas")
        
        import bs4
        print("✅ beautifulsoup4")
        
        from dapp_scraper.scrapers.dappradar import fetch_dappradar
        print("✅ dappradar scraper")
        
        from dapp_scraper.store import store_records
        print("✅ store module")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Try running: pip install -r requirements.txt")
        return False

def main():
    """Run all tests"""
    print("🧪 DApp Scraper Setup Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test configuration
    if test_api_configuration():
        tests_passed += 1
    
    # Test database
    if test_database_connection():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("   1. Run: python scripts/init_db.py (if tables not found)")
        print("   2. Run: python scripts/run_fetch_all.py test")
        print("   3. Run: python scripts/run_fetch_all.py")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 