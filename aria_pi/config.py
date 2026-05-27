"""Config loading and validation for ARIA-PI.

Loads `config.yaml` (or a path passed via CLI) plus environment variables from
`.env`, validates required secrets are present, and exposes a single `Config`
dataclass that is passed to every stage and client. No global state.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


REQUIRED_ENV_VARS = ("ANTHROPIC_API_KEY", "TAVILY_API_KEY")


@dataclass
class ClaudeConfig:
    model: str = "claude-opus-4-7"
    max_tokens: int = 4096
    temperature: float = 0.2
    max_retries: int = 3
    api_key: str = ""


@dataclass
class PubMedConfig:
    base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    default_max_results: int = 20
    requests_per_second_no_key: int = 3
    requests_per_second_with_key: int = 10
    api_key: str = ""
    email: str = ""


@dataclass
class NIHReporterConfig:
    base_url: str = "https://api.reporter.nih.gov/v2"
    default_fiscal_years_back: int = 5


@dataclass
class ClinicalTrialsConfig:
    base_url: str = "https://clinicaltrials.gov/api/v2"
    max_results: int = 50


@dataclass
class SECEdgarConfig:
    full_text_search_url: str = "https://efts.sec.gov/LATEST/search-index"
    submissions_url: str = "https://data.sec.gov/submissions"
    company_search_url: str = "https://www.sec.gov/cgi-bin/browse-edgar"
    user_agent: str = "ARIA-PI research@example.com"


@dataclass
class OpenAlexConfig:
    base_url: str = "https://api.openalex.org"
    mailto: str = ""


@dataclass
class TavilyConfig:
    base_url: str = "https://api.tavily.com"
    default_max_results: int = 5
    api_key: str = ""


@dataclass
class UNCConfig:
    primary_affiliation: str = "University of North Carolina at Chapel Hill"
    affiliation_aliases: list[str] = field(default_factory=list)


@dataclass
class SelectionConfig:
    top_n: int = 5
    min_score: int = 55
    relationship_active_window_months: int = 24


@dataclass
class VerificationConfig:
    min_sources_per_claim: int = 2
    banned_source_patterns: list[str] = field(default_factory=list)
    banned_phrases: list[str] = field(default_factory=list)


@dataclass
class OutputConfig:
    dir: str = "output"
    blocked_dir: str = "output/blocked"
    logs_dir: str = "logs"


@dataclass
class Config:
    claude: ClaudeConfig
    pubmed: PubMedConfig
    nih_reporter: NIHReporterConfig
    clinicaltrials: ClinicalTrialsConfig
    sec_edgar: SECEdgarConfig
    openalex: OpenAlexConfig
    tavily: TavilyConfig
    unc: UNCConfig
    selection: SelectionConfig
    verification: VerificationConfig
    output: OutputConfig
    data_dir: Path
    project_root: Path


def _coerce(section: dict[str, Any] | None, dataclass_type):
    """Build a dataclass from a YAML dict, ignoring unknown keys."""
    section = section or {}
    field_names = {f.name for f in dataclass_type.__dataclass_fields__.values()}
    return dataclass_type(**{k: v for k, v in section.items() if k in field_names})


def load_config(config_path: str | Path | None = None) -> Config:
    """Load and validate ARIA-PI config.

    Reads YAML, overlays environment-driven secrets, and verifies that
    required env vars are present. Raises EnvironmentError with a clear
    message listing missing keys.
    """
    load_dotenv()

    project_root = Path(__file__).resolve().parent.parent
    if config_path is None:
        config_path = project_root / "config.yaml"
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. "
            "Copy config.yaml from the repo root or pass --config."
        )

    with config_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    missing = [k for k in REQUIRED_ENV_VARS if not os.getenv(k)]
    if missing:
        raise EnvironmentError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in keys."
        )

    claude = _coerce(raw.get("claude"), ClaudeConfig)
    claude.api_key = os.environ["ANTHROPIC_API_KEY"]

    pubmed = _coerce(raw.get("pubmed"), PubMedConfig)
    pubmed.api_key = os.getenv("NCBI_API_KEY", "")
    pubmed.email = os.getenv("NCBI_EMAIL", "")

    tavily = _coerce(raw.get("tavily"), TavilyConfig)
    tavily.api_key = os.environ["TAVILY_API_KEY"]

    openalex = _coerce(raw.get("openalex"), OpenAlexConfig)
    openalex.mailto = os.getenv("ARIA_PI_CONTACT_EMAIL", "")

    sec_edgar = _coerce(raw.get("sec_edgar"), SECEdgarConfig)
    if os.getenv("ARIA_PI_CONTACT_EMAIL"):
        sec_edgar.user_agent = f"ARIA-PI {os.environ['ARIA_PI_CONTACT_EMAIL']}"

    nih_reporter = _coerce(raw.get("nih_reporter"), NIHReporterConfig)
    clinicaltrials = _coerce(raw.get("clinicaltrials"), ClinicalTrialsConfig)
    unc = _coerce(raw.get("unc"), UNCConfig)
    selection = _coerce(raw.get("selection"), SelectionConfig)
    verification = _coerce(raw.get("verification"), VerificationConfig)
    output = _coerce(raw.get("output"), OutputConfig)

    paths_section = raw.get("paths") or {}
    data_dir = project_root / paths_section.get("data_dir", "aria_pi/data")

    return Config(
        claude=claude,
        pubmed=pubmed,
        nih_reporter=nih_reporter,
        clinicaltrials=clinicaltrials,
        sec_edgar=sec_edgar,
        openalex=openalex,
        tavily=tavily,
        unc=unc,
        selection=selection,
        verification=verification,
        output=output,
        data_dir=data_dir,
        project_root=project_root,
    )
