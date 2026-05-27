"""Cross-cutting utilities: logging, source tagging, deduplication, formatting."""

from .deduplicator import Deduplicator
from .formatter import Formatter
from .logger import get_logger
from .source_tagger import SourceTagger

__all__ = ["Deduplicator", "Formatter", "SourceTagger", "get_logger"]
