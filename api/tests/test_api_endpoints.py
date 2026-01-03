"""
Minimal API endpoint tests using starlette.testclient.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_snapshot_endpoint():
    """Test the snapshot endpoint."""
    response = client.get("/snapshot")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "system_overview" in data
    assert "top_5_longest_songs" in data
    assert "recently_played_songs" in data
    assert "song_count_by_rating" in data
    assert "extremes" in data

if __name__ == "__main__":
    test_health_endpoint()
    test_snapshot_endpoint()
    print("All tests passed!")