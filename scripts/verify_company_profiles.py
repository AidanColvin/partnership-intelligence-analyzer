import sys
from pathlib import Path
base = Path("data/processed/company-profiles")
for company in ["apple", "google", "pfizer"]:
    files = ["raw.txt", "profile.json", "summary.json", "metadata.json", f"{company}-profile.md", "deliverable.pdf"]
    for f in files:
        if not (base / company / f).exists(): print(f"Error: {f} missing for {company}"); sys.exit(1)
print("Success")
