import pytest

@pytest.mark.parametrize("company, dept", [
    ("apple", "computer_science"),
    ("google", "computer_science"),
    ("pfizer", "public_health")
])
def test_valid_alignment(client, company, dept):
    response = client.post("/api/align", json={"department_id": dept, "corporate_slug": company})
    assert response.status_code == 200
    data = response.json()
    assert data["department_id"] == dept
    assert data["corporate_slug"] == company
    assert 0 <= data["score"] <= 100
    assert data["intensity_metric"] >= 0
    assert data["word_count"] > 0
    assert data["match_count"] >= 0
