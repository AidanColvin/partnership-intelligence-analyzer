# FILE: backend/tests/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_apple_request():
    response = client.post("/api/align", json={"department_id": "computer_science", "corporate_slug": "apple"})
    assert response.status_code == 200
    data = response.json()
    assert data["corporate_slug"] == "apple"
    assert "score" in data

def test_valid_google_request():
    response = client.post("/api/align", json={"department_id": "computer_science", "corporate_slug": "google"})
    assert response.status_code == 200

def test_valid_pfizer_request():
    response = client.post("/api/align", json={"department_id": "public_health", "corporate_slug": "pfizer"})
    assert response.status_code == 200

def test_invalid_department():
    response = client.post("/api/align", json={"department_id": "invalid_dept", "corporate_slug": "apple"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Unknown department"

def test_missing_report():
    response = client.post("/api/align", json={"department_id": "computer_science", "corporate_slug": "nonexistent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Missing report"
