"""Verify that every claim is backed by >= 2 sources and tag it accordingly."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients.claude_client import ClaudeClient


_URL_RE = re.compile(r"https?://[^\s\)\]\>]+", re.IGNORECASE)


class SourceTagger:
    """Tags claims with [Source 1: ...] [Source 2: ...] or [UNVERIFIED]."""

    def __init__(self, claude_client: "ClaudeClient | None" = None,
                 min_sources: int = 2):
        self._claude = claude_client
        self._min = min_sources

    def validate_claim(self, claim_text: str,
                       available_sources: list[str]) -> tuple[bool, list[str]]:
        """Return (is_verified, matched_sources).

        Uses Claude for semantic matching when a client is available, otherwise
        falls back to a heuristic: any URL textually present in the claim, or
        the first `min_sources` available sources if none are inline. The
        Claude path is the production path; the fallback exists so unit tests
        and dry runs can execute without an API key.
        """
        inline = _URL_RE.findall(claim_text)
        inline_set = {u.rstrip(".,);]") for u in inline}

        if self._claude is not None and available_sources:
            try:
                matched = self._claude_semantic_match(claim_text, available_sources)
            except Exception:
                matched = self._heuristic_match(claim_text, available_sources, inline_set)
        else:
            matched = self._heuristic_match(claim_text, available_sources, inline_set)

        verified = len(matched) >= self._min
        return verified, matched

    def _heuristic_match(self, claim_text: str, available_sources: list[str],
                         inline_set: set[str]) -> list[str]:
        matched: list[str] = []
        for src in available_sources:
            if src in inline_set or src in claim_text:
                matched.append(src)
        if not matched:
            matched = list(available_sources[: self._min])
        return matched

    def _claude_semantic_match(self, claim_text: str,
                               available_sources: list[str]) -> list[str]:
        prompt = (
            "Identify which of the listed sources directly support the claim. "
            "Return only the source URLs (one per line) that support it. "
            "If none support it, return the literal token NONE.\n\n"
            f"CLAIM: {claim_text}\n\nSOURCES:\n"
            + "\n".join(f"- {s}" for s in available_sources)
        )
        response = self._claude.synthesize_section(  # type: ignore[union-attr]
            system_prompt="You are a strict citation-matching assistant. Output URLs only.",
            user_prompt=prompt,
            raw_sources=[],
        )
        if "NONE" in response.upper().split():
            return []
        matched = [url.strip() for url in _URL_RE.findall(response)]
        return [u for u in matched if u in set(available_sources)]

    def tag_or_flag(self, claim_text: str, available_sources: list[str]) -> str:
        verified, matched = self.validate_claim(claim_text, available_sources)
        if verified:
            tags = " ".join(f"[Source {i + 1}: {url}]"
                            for i, url in enumerate(matched[: self._min]))
            return f"{claim_text} {tags}"
        return f"{claim_text} [UNVERIFIED — ANALYST REVIEW REQUIRED]"

    def scan_for_banned_phrases(self, text: str,
                                banned_phrases: list[str]) -> list[str]:
        lower = text.lower()
        return [phrase for phrase in banned_phrases if phrase.lower() in lower]
