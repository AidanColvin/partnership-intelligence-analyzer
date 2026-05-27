"""Per-company partnership intelligence profile (stage 4 output)."""
from __future__ import annotations

from dataclasses import dataclass, field

from .claim import Claim
from .company import Company


@dataclass
class Profile:
    company: Company
    overview: list[Claim] = field(default_factory=list)
    pipeline_programs: list[dict] = field(default_factory=list)
    partnering_history: list[dict] = field(default_factory=list)
    unc_alignments: list[dict] = field(default_factory=list)
    unc_offerings: list[dict] = field(default_factory=list)
    key_signals: list[Claim] = field(default_factory=list)
    partnership_flag: str = ""
    existing_unc_tie: str = "none"
    existing_unc_tie_description: str = ""
