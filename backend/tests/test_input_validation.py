def test_missing_fields(client):
    response = client.post("/api/align", json={"department_id": "computer_science"})
    assert response.status_code == 422

def test_malformed_json(client):
    response = client.post("/api/align", data="not json")
    assert response.status_code == 422

def test_empty_strings(client):
    response = client.post("/api/align", json={"department_id": "", "corporate_slug": ""})
    assert response.status_code == 400
