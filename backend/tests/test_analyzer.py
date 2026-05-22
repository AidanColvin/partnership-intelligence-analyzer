# FILE: backend/tests/test_analyzer.py
from app.core.analyzer import analyze_text

def test_exact_matching():
    text = "We use machine learning and computer vision."
    res = analyze_text(text, ["machine learning", "computer vision"])
    assert res["match_count"] == 2
    assert res["total_words"] == 7

def test_no_false_positive():
    text = "The union is immunizing workers."
    res = analyze_text(text, ["union", "immunization"])
    assert res["match_count"] == 1

def test_empty_text():
    res = analyze_text("", ["machine learning"])
    assert res["match_count"] == 0
    assert res["total_words"] == 0
    assert res["score"] == 0.0
    assert res["intensity_metric"] == 0.0

def test_score_capping():
    text = "data data data data"
    res = analyze_text(text, ["data"])
    assert res["intensity_metric"] == 1000.0
    assert res["score"] == 100.0

def test_case_insensitivity():
    text = "Machine Learning is powerful."
    res = analyze_text(text, ["machine learning"])
    assert res["match_count"] == 1
