import json, re, os
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    company: str
    overallScore: int
    breakdowns: List[dict]

def run_alignment_analysis(company_name: str, report_text: str) -> AnalysisResult:
    """
    # takes: company_name (str), report_text (str)
    # does: Maps unstructured corporate report text to UNC departments using keyword frequency arrays
    # returns: AnalysisResult object containing score and department matches
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(base_dir, 'data', 'unc_departments.json'), 'r') as f:
        unc_data = json.load(f)
    
    text_lower = report_text.lower()
    total_words = len(re.findall(r'\w+', text_lower)) or 1
    results = []
    total_matches = 0
    
    for dept, keywords in unc_data.items():
        count = sum(len(re.findall(rf'\b{re.escape(k)}\b', text_lower)) for k in keywords)
        if count > 0:
            results.append({"department": dept.upper(), "matchCount": count})
            total_matches += count
            
    return AnalysisResult(
        company=company_name,
        overallScore=min(int((total_matches / total_words) * 5000), 100),
        breakdowns=results
    )
