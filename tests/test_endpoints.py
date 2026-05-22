import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_align_endpoint_success():
    """
    # takes: None
    # does: Asserts /api/align endpoint successfully responds to cached company requests
    # returns: None
    """
    response = client.post("/api/align", json={"companyName": "apple"})
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "apple"
    assert "overallScore" in data
    assert "breakdowns" in data

def test_align_endpoint_not_found():
    """
    # takes: None
    # does: Asserts /api/align handles uncached company queries with a strict 404 response
    # returns: None
    """
    response = client.post("/api/align", json={"companyName": "nonexistent_corp"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"
