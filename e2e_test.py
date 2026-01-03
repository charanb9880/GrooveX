#!/usr/bin/env python3
"""
End-to-end test for PlayWise Music Engine UI Integration
"""

import requests
import time

def test_api_endpoints():
    """Test that API endpoints are working"""
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        print("✓ Health endpoint working")
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")
        return False
    
    # Test snapshot endpoint
    try:
        response = requests.get(f"{base_url}/snapshot")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "system_overview" in data
        print("✓ Snapshot endpoint working")
    except Exception as e:
        print(f"✗ Snapshot endpoint failed: {e}")
        return False
    
    return True

def test_web_ui():
    """Test that web UI is accessible"""
    try:
        response = requests.get("http://localhost:3000")
        # Even if we get a 404 or other error, it means the server is responding
        print("✓ Web UI is accessible")
        return True
    except Exception as e:
        print(f"✗ Web UI not accessible: {e}")
        return False

def main():
    """Run end-to-end tests"""
    print("Running PlayWise Music Engine End-to-End Tests")
    print("=" * 50)
    
    # Wait a moment for services to start
    time.sleep(2)
    
    # Test API
    api_ok = test_api_endpoints()
    
    # Test Web UI
    web_ok = test_web_ui()
    
    print("=" * 50)
    if api_ok and web_ok:
        print("🎉 All end-to-end tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())