import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.analyzer import analyze_text

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "unc_departments.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

class AlignmentRequest(BaseModel):
    department_id: str
    corporate_slug: str

@router.post("/align")
def align_department(req: AlignmentRequest):
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            deps = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")

    if req.department_id not in deps:
        raise HTTPException(status_code=400, detail="Unknown department")

    keywords = deps[req.department_id]
    report_path = os.path.join(REPORTS_DIR, f"{req.corporate_slug}.txt")

    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Missing report")

    with open(report_path, "r", encoding="utf-8") as f:
        text = f.read()

    result = analyze_text(text, keywords)

    return {
        "department_id": req.department_id,
        "corporate_slug": req.corporate_slug,
        "score": result["score"],
        "intensity_metric": result["intensity_metric"],
        "word_count": result["total_words"],
        "match_count": result["match_count"],
    }
