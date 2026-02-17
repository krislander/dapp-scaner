#!/usr/bin/env python3
"""
Simple script to test DappRadar API connectivity and status
"""
import requests
from configparser import ConfigParser
import os
import sys
from datetime import datetime

def test_dappradar_api():
    """
    Test if DappRadar API is accessible and responding
    """
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    cfg = ConfigParser()
    cfg.read(config_path)
    
    API_KEY = cfg["dappradar"]["api_key"]
    API_ORIGIN = cfg["dappradar"]["api_origin"]
    
    print("=" * 60)
    print("🔍 Testing DappRadar API Connection")
    print("=" * 60)
    print(f"📍 API Origin: {API_ORIGIN}")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Test endpoint with minimal request
    test_endpoint = f"{API_ORIGIN}dapps/top/uaw"
    headers = {"x-api-key": API_KEY}
    params = {
        "category": "games",
        "range": "30d",
        "top": 1  # Request only 1 result for quick test
    }
    
    try:
        print(f"🌐 Sending request to: {test_endpoint}")
        print(f"📦 Parameters: {params}")
        print()
        
        # Make the request with timeout
        response = requests.get(test_endpoint, headers=headers, params=params, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
        print(f"📏 Response Size: {len(response.content)} bytes")
        print()
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            print("✅ API Status: WORKING")
            print(f"📈 Sample Data Retrieved: {len(results)} DApp(s)")
            
            if results:
                sample = results[0]
                print(f"📱 Sample DApp: {sample.get('name', 'N/A')}")
                print(f"   Category: {sample.get('categories', ['N/A'])[0] if sample.get('categories') else 'N/A'}")
                print(f"   Chains: {len(sample.get('chains', []))}")
            
            print()
            print("=" * 60)
            print("✨ DappRadar API is UP and RUNNING!")
            print("=" * 60)
            return True
            
        elif response.status_code == 401:
            print("❌ API Status: AUTHENTICATION FAILED")
            print("🔑 Error: Invalid or expired API key")
            print("💡 Tip: Check your API key in config/config.ini")
            print()
            print("=" * 60)
            return False
            
        elif response.status_code == 429:
            print("⚠️  API Status: RATE LIMITED")
            print("🚦 Error: Too many requests")
            print("💡 Tip: Wait a moment and try again")
            print()
            print("=" * 60)
            return False
            
        else:
            print(f"⚠️  API Status: UNEXPECTED RESPONSE")
            print(f"📝 Response: {response.text[:200]}")
            print()
            print("=" * 60)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API Status: TIMEOUT")
        print("⏱️  Error: Request took too long (>10s)")
        print("💡 Tip: Check your internet connection")
        print()
        print("=" * 60)
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ API Status: CONNECTION ERROR")
        print("🌐 Error: Could not connect to DappRadar")
        print("💡 Tip: Check your internet connection or DNS")
        print()
        print("=" * 60)
        return False
        
    except Exception as e:
        print(f"❌ API Status: ERROR")
        print(f"🐛 Error: {str(e)}")
        print()
        print("=" * 60)
        return False


if __name__ == "__main__":
    try:
        success = test_dappradar_api()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)

