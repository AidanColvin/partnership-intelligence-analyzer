def test_unknown_department(client):
    response = client.post("/api/align", json={"department_id": "fake_dept", "corporate_slug": "apple"})
    assert response.status_code == 400
    assert "Unknown department" in response.json()["detail"]

def test_missing_report(client):
    response = client.post("/api/align", json={"department_id": "computer_science", "corporate_slug": "fake_corp"})
    assert response.status_code == 404
    assert "Missing report" in response.json()["detail"]
