from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from core.analyzer import run_alignment_analysis

router = APIRouter()
class Req(BaseModel): companyName: str

@router.post("/align")
async def align(req: Req):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', f"{req.companyName.lower()}.txt")
    if not os.path.exists(path): raise HTTPException(status_code=404, detail="Company not found")
    with open(path, 'r') as f: return run_alignment_analysis(req.companyName, f.read())
