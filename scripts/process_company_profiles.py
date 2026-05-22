import json, sys, datetime
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "backend"))
from app.core.analyzer import analyze_text

def run():
    deps = json.load(open(repo_root / "backend" / "app" / "data" / "unc_departments.json"))
    keywords = deps["computer_science"] + deps["health_data"] + deps["oncology"]
    out_base = repo_root / "data" / "processed" / "company-profiles"
    
    for company in ["apple", "google", "pfizer"]:
        text = (repo_root / "backend" / "app" / "reports" / f"{company}.txt").read_text()
        out_dir = out_base / company
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "raw.txt").write_text(text)
        
        res = analyze_text(text, keywords)
        profile = {"company": company, "generated_at": datetime.datetime.now().isoformat(), "word_count": res["total_words"], "score": res["score"], "matches": res["match_count"]}
        
        (out_dir / "profile.json").write_text(json.dumps(profile, indent=4))
        (out_dir / "summary.json").write_text(json.dumps({"company": company, "score": res["score"]}, indent=4))
        (out_dir / "matches.json").write_text(json.dumps({"matches": res["match_count"]}, indent=4))
        (out_dir / "metadata.json").write_text(json.dumps({"ts": datetime.datetime.now().isoformat()}, indent=4))

if __name__ == "__main__":
    run()
