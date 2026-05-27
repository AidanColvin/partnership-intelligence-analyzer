"""A single factual statement that must be backed by >= 2 sources."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Claim:
    text: str
    sources: list[str] = field(default_factory=list)
    is_verified: bool = False
    stage: str = ""
    company_name: str | None = None
    unverified_reason: str | None = None

    def to_markdown(self) -> str:
        if not self.is_verified:
            reason = self.unverified_reason or "needs analyst review"
            return f"{self.text} [UNVERIFIED — {reason.upper()}]"
        tags = " ".join(f"[Source {i + 1}: {url}]" for i, url in enumerate(self.sources))
        return f"{self.text} {tags}"
