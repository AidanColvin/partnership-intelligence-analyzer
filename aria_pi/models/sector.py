"""Sector-level output produced by stage 1 (sector_overview)."""
from __future__ import annotations

from dataclasses import dataclass, field

from .claim import Claim


@dataclass
class SectorOverview:
    name: str
    slug: str
    definition: str = ""
    market_size_statement: str = ""
    why_now_signals: list[Claim] = field(default_factory=list)
    nc_context: list[Claim] = field(default_factory=list)
    unc_units: list[dict] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
