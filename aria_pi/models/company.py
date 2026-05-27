"""Company record used through selection, profiling, and verification."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Company:
    name: str
    domain: str | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    company_type: str | None = None
    employee_count: int | None = None
    founded_year: int | None = None
    revenue: float | None = None
    stock_ticker: str | None = None
    parent_company: str | None = None
    is_public: bool = False
    risk_flag: bool = False
    risk_flag_reason: str | None = None
    risk_override: bool = False
    risk_override_reason: str | None = None
    selection_score: float = 0.0
    selection_criteria_scores: dict[str, float] = field(default_factory=dict)
    exclusion_reason: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def slug(self) -> str:
        return (
            self.name.lower()
            .replace(",", "")
            .replace(".", "")
            .replace("'", "")
            .replace(" ", "-")
        )
