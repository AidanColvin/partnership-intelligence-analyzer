from app.core.analyzer import analyze_text

def test_exact_boundary_matching():
    res = analyze_text("The union works on immunization.", ["union", "immunization"])
    assert res["match_count"] == 2

def test_no_substring_false_positives():
    res = analyze_text("immunization", ["union"])
    assert res["match_count"] == 0

def test_empty_text():
    res = analyze_text("", ["apple"])
    assert res["match_count"] == 0
    assert res["total_words"] == 0
    assert res["intensity_metric"] == 0
    assert res["score"] == 0

def test_zero_keywords():
    res = analyze_text("some words here", [])
    assert res["match_count"] == 0
    assert res["total_words"] == 3

def test_repeated_keywords():
    res = analyze_text("data data data data", ["data"])
    assert res["match_count"] == 4
    assert res["total_words"] == 4
    assert res["intensity_metric"] == 1000.0
    assert res["score"] == 100.0
