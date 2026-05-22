import sys
import json
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent.parent
    out_dir = repo_root / "data" / "processed" / "company-profiles"
    companies = ["apple", "google", "pfizer"]
    
    errors = 0
    
    for company in companies:
        comp_dir = out_dir / company
        if not comp_dir.exists():
            print(f"FAIL: Missing directory {comp_dir}")
            errors += 1
            continue
            
        profile_path = comp_dir / "profile.json"
        summary_path = comp_dir / "summary.json"
        raw_path = comp_dir / "raw.txt"
        
        for p in [profile_path, summary_path, raw_path]:
            if not p.exists():
                print(f"FAIL: Missing file {p}")
                errors += 1
                
        if errors > 0:
            continue
            
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        if not raw_text.strip():
            print(f"FAIL: {raw_path} is empty")
            errors += 1
            
        if profile.get("company") != company:
            print(f"FAIL: profile.json company mismatch for {company}")
            errors += 1
            
        if summary.get("company") != company:
            print(f"FAIL: summary.json company mismatch for {company}")
            errors += 1
            
        if "top_department" not in summary:
            print(f"FAIL: summary.json missing top_department for {company}")
            errors += 1
            
        if not isinstance(profile.get("word_count"), int):
            print(f"FAIL: profile.json word_count invalid for {company}")
            errors += 1
            
    if errors == 0:
        print("SUCCESS: All processed outputs verified successfully.")
        sys.exit(0)
    else:
        print(f"FAILED with {errors} errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
