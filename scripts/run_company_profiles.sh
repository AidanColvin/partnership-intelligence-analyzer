#!/usr/bin/env bash
set -euo pipefail
python3 scripts/process_company_profiles.py
python3 scripts/generate_company_report.py
python3 scripts/verify_company_profiles.py
