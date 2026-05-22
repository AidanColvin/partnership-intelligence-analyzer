import pytest
from core.analyzer import run_alignment_analysis

def test_run_alignment_analysis_success():
    """
    # takes: None
    # does: Asserts analyzer correctly processes text matching criteria keywords
    # returns: None
    """
    sample_text = "This department focuses on computer vision and machine learning protocols."
    result = run_alignment_analysis("TestCompany", sample_text)
    
    assert result.company == "TestCompany"
    assert result.overallScore > 0
    # Confirm it hit the computer_science department cluster
    cs_match = next((b for b in result.breakdowns if b["department"] == "COMPUTER_SCIENCE"), None)
    assert cs_match is not None
    assert cs_match["matchCount"] == 2

def test_run_alignment_analysis_zero_matches():
    """
    # takes: None
    # does: Asserts analyzer handles completely irrelevant text gracefully
    # returns: None
    """
    irrelevant_text = "Baking bread requires flour, yeast, water, and heat inside a warm oven."
    result = run_alignment_analysis("BreadCo", irrelevant_text)
    
    assert result.overallScore == 0
    assert len(result.breakdowns) == 0
