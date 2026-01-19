import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
