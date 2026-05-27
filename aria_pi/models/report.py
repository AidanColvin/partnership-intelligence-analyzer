"""Top-level report container (final assembled artifact)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .profile import Profile
from .sector import SectorOverview


@dataclass
class Report:
    sector: SectorOverview
    internal_map: dict = field(default_factory=dict)
    company_selection: dict = field(default_factory=dict)
    profiles: list[Profile] = field(default_factory=list)
    value_proposition: dict = field(default_factory=dict)
    talking_points: dict = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "0.1.0"
    reviewer: str = ""
    verification_status: str = "pending"
