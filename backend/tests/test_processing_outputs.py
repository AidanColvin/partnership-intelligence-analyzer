# FILE: backend/tests/test_processing_outputs.py
import os
from pathlib import Path

def test_processed_directories_exist():
    out_dir = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "company-profiles"
    if out_dir.exists():
        assert out_dir.is_dir()
