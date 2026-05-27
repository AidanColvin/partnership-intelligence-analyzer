"""Deduplication helpers for faculty, sources, and company names."""
from __future__ import annotations

import re
from urllib.parse import urlparse

try:
    from fuzzywuzzy import fuzz  # type: ignore
except ImportError:  # pragma: no cover — fuzzywuzzy is a hard dependency
    fuzz = None


_TITLE_PREFIXES = ("dr.", "dr", "prof.", "prof", "mr.", "ms.", "mrs.")
_COMPANY_SUFFIXES = (
    "inc.", "inc", "incorporated", "llc", "l.l.c.", "ltd.", "ltd",
    "limited", "corp.", "corp", "corporation", "co.", "co", "company",
    "plc", "ag", "sa", "s.a.", "nv",
)


def _normalize_name(name: str) -> str:
    cleaned = name.strip().lower()
    for prefix in _TITLE_PREFIXES:
        if cleaned.startswith(prefix + " "):
            cleaned = cleaned[len(prefix) + 1:]
    return re.sub(r"\s+", " ", cleaned)


def _normalize_company(name: str) -> str:
    cleaned = name.strip().lower()
    cleaned = re.sub(r"[.,]", "", cleaned)
    tokens = cleaned.split()
    while tokens and tokens[-1] in {s.replace(".", "") for s in _COMPANY_SUFFIXES}:
        tokens.pop()
    return " ".join(tokens)


def _normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme}://{netloc}{path}" if parsed.scheme else f"{netloc}{path}"


class Deduplicator:
    def deduplicate_faculty(self, faculty_list: list[dict]) -> list[dict]:
        """Merge entries that refer to the same person; combine source lists."""
        merged: dict[str, dict] = {}
        for entry in faculty_list:
            key = _normalize_name(entry.get("name", ""))
            if not key:
                continue
            if key in merged:
                existing = merged[key]
                existing_sources = set(existing.get("sources", []))
                existing_sources.update(entry.get("sources", []))
                existing["sources"] = sorted(existing_sources)
                for field_name in ("title", "department", "school",
                                   "research_focus", "pubmed_url",
                                   "faculty_page_url"):
                    if not existing.get(field_name) and entry.get(field_name):
                        existing[field_name] = entry[field_name]
            else:
                merged[key] = dict(entry)
        return list(merged.values())

    def deduplicate_sources(self, sources: list[str]) -> list[str]:
        """Return a stable, order-preserving list of unique normalized URLs."""
        seen: set[str] = set()
        result: list[str] = []
        for url in sources:
            if not url:
                continue
            normalized = _normalize_url(url)
            if normalized in seen:
                continue
            seen.add(normalized)
            result.append(url)
        return result

    def deduplicate_companies(self, companies: list[str], threshold: int = 90) -> list[str]:
        """Fuzzy-merge company names. Returns canonical (first-seen) names."""
        canonical: list[tuple[str, str]] = []  # (normalized, original)
        for raw in companies:
            normalized = _normalize_company(raw)
            if not normalized:
                continue
            matched = False
            for norm, _orig in canonical:
                if norm == normalized:
                    matched = True
                    break
                if fuzz is not None and fuzz.ratio(norm, normalized) >= threshold:
                    matched = True
                    break
            if not matched:
                canonical.append((normalized, raw.strip()))
        return [orig for _norm, orig in canonical]
