# UNC–Industry Alignment Engine

A production-oriented full-stack platform for generating recruiter-grade company alignment profiles from structured institutional keyword mappings and corporate source materials. The system combines a FastAPI backend, a modular text-analysis core, a React frontend, and a batch reporting pipeline that saves raw text, machine-readable JSON artifacts, Markdown reports, and PDF outputs into a deterministic repository structure. [file:87][file:27]

This program is designed to do more than score keyword overlap. It provides an end-to-end workflow for ingesting company source text, normalizing and analyzing that text against department-aligned research themes, generating human-readable strategic profiles, and preserving every output in a format suitable for APIs, internal review, and polished recruiter-facing documents. [file:87][file:27]

## Overview

At its core, the system measures how well a company’s public strategic language aligns with university department priorities. It does this by loading department-specific keyword sets from structured configuration, scanning normalized company source text using boundary-safe regex matching, calculating normalized frequency and intensity metrics, and packaging those results into structured API and reporting outputs. [file:87]

The platform is intentionally layered so the algorithmic logic is independent from the web layer and the reporting layer. That separation makes the system easier to test, easier to extend into scheduled or queued jobs, and easier to present as enterprise-style architecture rather than a one-off script. [file:87]

## System Goals

The program is built to support five operational goals:

- Analyze company text against institutional keyword buckets. [file:87]
- Return deterministic JSON output through a FastAPI interface. [file:87]
- Generate full company profile documents in Markdown and PDF formats. [file:87][file:27]
- Preserve the exact processed raw text used to generate each report. [file:87]
- Support repeatable, safe reruns across a fixed company set such as Apple, Google, and Pfizer. [file:87]

The reporting layer is modeled after a more polished strategic profile format rather than a simple technical dump. The attached Sanofi profile shows the target style: narrative overview, company facts, UNC connection framing, talking points, and an explicit references section. [file:27]

## Architecture

```text
Frontend (React/Vite)
        |
        | HTTP POST /api/align
        v
FastAPI Backend
        |
        | validated request
        v
Analyzer Core
        |
        | reads structured config + company report text
        v
Data Layer
        |
        | writes processed outputs
        v
Profile Output Pipeline
```

The architecture is organized into four major tiers: gateway, API, algorithmic core, and reporting/data persistence. The frontend acts as the user-facing control layer, the FastAPI service validates and routes requests, the analyzer computes keyword alignment metrics, and the reporting pipeline materializes raw and generated artifacts into a structured folder tree. [file:87]

This design is intentional because each layer has a single purpose. The web layer handles transport and validation, the core engine handles lexical analysis and scoring, and the output layer handles report generation and file persistence. [file:87]

## Repository Structure

A representative repository layout for the system includes backend, frontend, scripts, and processed output directories. The pasted program description and planning notes repeatedly center the implementation around FastAPI, React, `scripts/`, and a generated output path rooted under `data/processed/company-profiles/`. [file:87]

```text
.
├── README.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── endpoints.py
│   │   ├── core/
│   │   │   └── analyzer.py
│   │   ├── data/
│   │   │   └── unc_departments.json
│   │   └── reports/
│   │       ├── apple.txt
│   │       ├── google.txt
│   │       └── pfizer.txt
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── tests/
│   └── package.json
├── scripts/
│   ├── process_company_profiles.py
│   ├── generate_company_report.py
│   ├── verify_company_profiles.py
│   └── run_company_profiles.sh
└── data/
    └── processed/
        └── company-profiles/
            ├── apple/
            ├── google/
            └── pfizer/
```

## Backend Layer

### `backend/app/main.py`

This file is the FastAPI bootstrapper and gateway entry point for the backend service. In the program plan, it is responsible for creating the FastAPI application, mounting CORS middleware, and including the API router that exposes the alignment endpoint. [file:87]

Its purpose is architectural rather than computational. It should stay thin so the app bootstrap remains easy to reason about, easy to deploy under Uvicorn, and easy to modify when environment-specific middleware or deployment concerns change. [file:87]

### `backend/app/api/endpoints.py`

This file acts as the request intake and validation controller for the service. The planning notes specify that it should expose `POST /api/align`, define a typed `AlignmentRequest` payload with `department_id` and `corporate_slug`, validate the department against structured JSON configuration, validate report-file existence, call the analyzer, and return a structured JSON payload containing `score`, `intensity_metric`, `word_count`, and `match_count`. [file:87]

This layer is where transport logic ends and computational logic begins. Its value is that malformed inputs, unknown departments, and missing company reports are handled as explicit HTTP outcomes instead of producing low-level exceptions inside the analyzer. [file:87]

### `backend/app/core/analyzer.py`

This file contains the pure text-analysis logic. The program plan defines it as a function that takes raw text and a list of keywords, uses a regex pattern of the form `rf'\b{re.escape(keyword)}\b'`, counts exact matches, computes word totals, calculates an intensity metric per 1,000 words, and caps the final score at 100. [file:87]

This is the most portable part of the system because it is intentionally decoupled from FastAPI and file I/O. The planning notes emphasize that this separation allows the analyzer to be unit-tested independently and later reused in queues, pipelines, or larger document-processing workflows without refactoring the core algorithm. [file:87]

## Data Layer

### `backend/app/data/unc_departments.json`

This file is the declarative metadata layer mapping department identifiers to keyword buckets. The program description treats this as a business-logic configuration asset rather than executable code, allowing department definitions to be updated without rewriting Python logic. [file:87]

That design matters because it separates institutional mapping decisions from the scoring engine. It also makes the system easier to audit, easier to expand to additional departments, and easier to explain to non-engineering stakeholders. [file:87]

### `backend/app/reports/*.txt`

These files hold locally stored source material for target companies such as Apple, Google, and Pfizer. The planning notes position these files as a static data tier that avoids dependence on live external APIs at runtime and provides deterministic, testable inputs for repeated analysis. [file:87]

This local-first approach is a practical engineering choice. It reduces latency, avoids quota issues, prevents credential sprawl, and ensures that both tests and generated reports can be reproduced from known source inputs. [file:87]

## Reporting and Output Pipeline

A major extension of the program is the company-profile pipeline that writes both raw and generated artifacts into a structured output directory. The requested output path is `data/processed/company-profiles/<company>/`, and each company directory is expected to contain `raw.txt`, `profile.json`, `summary.json`, `matches.json`, `metadata.json`, `<company>-profile.md`, and `<company>-profile.pdf`. [file:87]

The purpose of this layer is traceability. It ensures that every generated report can be tied back to exact processed text and exact machine-readable intermediate outputs, which is important for reproducibility, debugging, and auditing. [file:87]

### Required output files

For each company, the pipeline is expected to generate:

- `raw.txt`: the exact normalized text used in analysis. [file:87]
- `profile.json`: the comprehensive machine-readable profile artifact. [file:87]
- `summary.json`: the concise top-line processing summary. [file:87]
- `matches.json`: department-by-department match detail. [file:87]
- `metadata.json`: run metadata including paths, timestamps, and pipeline version. [file:87]
- `<company>-profile.md`: the polished strategic profile in Markdown. [file:87][file:27]
- `<company>-profile.pdf`: the PDF version of the Markdown report. [file:87]

The pasted notes explicitly require deterministic reruns and safe overwrites. That means the pipeline should recreate or replace outputs consistently instead of appending partial artifacts or leaving mixed-state directories behind. [file:87]

## Batch Scripts

The planned scripting layer includes four important entry points:

### `scripts/process_company_profiles.py`

This script is the main batch processor. According to the specification, it must load or find source company text for Apple, Google, and Pfizer, normalize that text, save `raw.txt`, run analyzer-driven department matching, and write all required JSON and report outputs. [file:87]

### `scripts/generate_company_report.py`

This script is responsible for transforming structured analysis results into polished Markdown and PDF documents. The intended report structure is based on the attached Sanofi profile pattern: company overview, basic company information, UNC connection, talking points, and references. [file:87][file:27]

### `scripts/verify_company_profiles.py`

This script validates output completeness. The plan requires it to confirm that each required company directory exists, each required JSON file is present and parseable, and each Markdown and PDF file exists and is non-empty, with a nonzero exit code on failure. [file:87]

### `scripts/run_company_profiles.sh`

This shell script is the top-level orchestrator. The specification requires it to use `set -euo pipefail`, install dependencies if needed, run the processing script, run verification, and print a final success message. [file:87]

## Frontend Layer

The frontend is planned as a React application created with Vite. The notes specify a simple interface with department and corporate selectors, a button to trigger alignment, and loading, error, and result states rendered through a reusable form component and a dedicated API service module. [file:87]

This layer exists to make the analysis system interactive rather than batch-only. It mirrors the same contract enforced by the backend and provides a path for demonstration, manual QA, and eventual hosted deployment. [file:87]

### Key frontend files

- `frontend/src/components/AlignmentForm.jsx`: reusable input and submission component. [file:87]
- `frontend/src/pages/Home.jsx`: page-level wrapper rendering form and results. [file:87]
- `frontend/src/services/api.js`: fetch wrapper using `import.meta.env.VITE_BACKEND_URL` with localhost fallback. [file:87]
- `frontend/src/App.js` or `App.jsx`: top-level app wrapper. [file:87]

The frontend is expected to maintain three explicit UI states: loading, resolution, and error. The planning notes frame those states as important for production consistency because they prevent duplicate submissions, surface network or file errors clearly, and make the returned metrics understandable to the user. [file:87]

## Request and Data Flow

The intended request lifecycle is straightforward but disciplined:

1. A user selects a department and a company in the frontend. [file:87]
2. The frontend sends a `POST /api/align` request to the FastAPI backend. [file:87]
3. The backend validates the request body using a typed schema. [file:87]
4. The backend loads department keywords from JSON and loads the selected company report from disk. [file:87]
5. The analyzer computes exact-match keyword counts, total words, intensity, and score. [file:87]
6. The backend returns those metrics in JSON format. [file:87]
7. The reporting pipeline can then persist raw text and generate full Markdown and PDF company profiles from those results. [file:87][file:27]

This flow is intentionally simple because it keeps the system explainable and deterministic. Even so, it demonstrates important software-engineering concerns such as typed contracts, configuration-driven logic, reproducible data handling, and separate transport and compute layers. [file:87]

## Algorithmic Model

The algorithm uses exact-match boundary-aware regex matching rather than naive substring matching. The planning notes explicitly call out the need to avoid false positives such as matching `union` inside `immunization`, which is why the expected regex pattern is `rf'\b{re.escape(keyword)}\b'`. [file:87]

The analyzer then computes:

- `total_words = len(tokens)` [file:87]
- `match_count = sum(keyword counts)` [file:87]
- `intensity_metric = (match_count / total_words) * 1000` when `total_words > 0` [file:87]
- `score = min(100, intensity_metric / 10)` [file:87]

This normalization step matters because raw match counts are biased toward longer documents. By expressing the signal as matches per 1,000 words, the system produces a more comparable density measure across reports of different lengths. [file:87]

## Complexity

The planning notes describe the core matching loop as \(O(N \cdot M)\), where \(N\) is the document size and \(M\) is the size of the department keyword set. Because \(M\) is bounded by a relatively small configuration mapping, runtime behaves close to linear in typical use. [file:87]

Memory usage is approximately \(O(N)\) because the text and tokenized representation are loaded into memory during analysis. For small or medium corporate source reports, that is a practical tradeoff for deterministic, readable logic. [file:87]

## API Contract

The main backend endpoint is planned as:

```json
POST /api/align
{
  "department_id": "cs",
  "corporate_slug": "google"
}
```

The intended response includes:

```json
{
  "department_id": "cs",
  "corporate_slug": "google",
  "score": 42.5,
  "intensity_metric": 425.0,
  "word_count": 1000,
  "match_count": 425
}
```

The same planning notes expect explicit error outcomes such as a missing report returning 404 and an invalid department returning a request-validation or explicit application error depending on the implementation path. [file:87]

## Report Format

The report-generation requirement is not just to dump metrics into Markdown. The output is expected to resemble a polished strategic briefing document modeled on the attached Sanofi profile. That reference includes a professional title, company overview, basic company information, a UNC connection section, organized talking points, and a references section. [file:27]

Accordingly, each generated Markdown file is expected to include:

- `# <COMPANY> PROFILE` [file:87]
- `## Company Overview` [file:87]
- `## Basic Company Information` [file:87]
- `## UNC Connection` [file:87]
- `## Talking Points` with subsections for context and research alignment. [file:87]
- `## References` [file:87][file:27]

This matters because the system is trying to produce output that is both technically grounded and presentation-ready. The Markdown files support source control and review, while the PDFs support clean distribution. [file:87]

## Testing Strategy

The backend is expected to include unit tests for the analyzer and API tests for endpoints. The planning notes specifically call for analyzer tests validating exact matching, false-positive prevention, empty-text handling, and score capping, plus endpoint tests covering valid requests, missing reports, invalid departments, and JSON response structure. [file:87]

The frontend is expected to include at least a basic render test, and the extended pipeline plan also calls for tests around directory creation, JSON serialization, Markdown generation, rerun behavior, and verification logic. That testing posture is a strong architectural signal because it treats the system as a real software product rather than just an interactive demo. [file:87]

## Deployment and Environment Strategy

The intended local stack is split between a FastAPI backend and a Vite-powered React frontend. The frontend is expected to read the backend base URL from `import.meta.env.VITE_BACKEND_URL`, with localhost fallback for development, allowing the same codebase to move between local and hosted environments without hardcoded URL changes. [file:87]

The planning notes also repeatedly frame the production deployment pattern as decoupled frontend and backend hosting, such as Vercel for the frontend and Render for the API service. That separation reflects a standard modern full-stack deployment model in which static client delivery and compute-backed API runtime can scale independently. [file:87]

## Why This Project Is Strong

This program is compelling because it demonstrates multiple layers of engineering maturity at once:

- Config-driven business logic rather than hardcoded matching rules. [file:87]
- A pure computational core isolated from transport concerns. [file:87]
- Typed API contracts and explicit error handling. [file:87]
- Deterministic local data inputs for reproducibility. [file:87]
- Structured raw and generated artifact persistence. [file:87]
- A reporting layer that translates machine analysis into decision-ready documents. [file:87][file:27]

In other words, the project does not just show that a score can be computed. It shows that a full system can be architected, tested, operated, and extended in a way that resembles real internal tooling or a production microservice-backed analytics workflow. [file:87]

## Local Development

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Full reporting pipeline

```bash
bash scripts/run_company_profiles.sh
```

This top-level run path is intended to install requirements if needed, process Apple, Google, and Pfizer, generate JSON plus Markdown and PDF outputs, and verify that every required artifact exists. [file:87]

## Output Locations

Successful runs are expected to produce:

```text
data/processed/company-profiles/apple/
data/processed/company-profiles/google/
data/processed/company-profiles/pfizer/
```

Each of those folders should contain raw text, structured JSON outputs, and polished report artifacts. The exact file set requested in the planning notes is `raw.txt`, `profile.json`, `summary.json`, `matches.json`, `metadata.json`, `<company>-profile.md`, and `<company>-profile.pdf`. [file:87]

## Future Extensions

The system as described is already structured for straightforward expansion. Natural next steps include more companies, richer departmental taxonomies, weighted keyword scoring, source URL capture, provenance tracking, asynchronous job execution, containerized deployment, and stronger CI verification around report generation and PDF integrity. [file:87]

Because the analyzer is isolated and the reporting layer is file-oriented, those enhancements can be added without redesigning the system from scratch. That is one of the strongest architectural properties of the current design. [file:87]

## References

- Program architecture, file layout, analyzer design, frontend plan, pipeline scripts, output schema, and workflow requirements from attached planning document. [file:87]
- Strategic company-profile structure and reporting style from attached Sanofi profile. [file:27]