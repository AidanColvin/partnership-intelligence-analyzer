# ARIA-PI

Automated Research Intelligence for Academic Partnership Intelligence.

ARIA-PI takes a sector name (and optional company list) and produces a
dual-source-cited Markdown partnership intelligence report intended for
human analyst review before delivery to a Business Development team.

## Status

v0.1 skeleton. Stage 1 (`sector_overview`) is implemented end-to-end;
remaining stages and clients are scaffolded with correct signatures
and will be filled in subsequent passes.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # then fill in keys
pytest
python -m aria_pi.orchestrator \
  --sector "oncology diagnostics" \
  --companies "Foundation Medicine,Guardant Health,Tempus AI" \
  --dry-run
```

## Layout

```
aria_pi/
  orchestrator.py       # CLI entry point, enforces stage order
  config.py             # Config loading + validation
  models/               # Dataclasses for claims, companies, profiles, reports
  clients/              # External API clients
  stages/               # The 8 pipeline stages
  utils/                # Source tagging, dedup, formatting, logging
  data/                 # Seeded UNC reference data
  tests/                # Unit tests + fixtures
```
