"""Structured JSON logging used across stages and clients."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Render log records as one-line JSON for easy parsing."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for attr in ("stage", "client", "endpoint", "status", "duration_ms",
                     "tokens_in", "tokens_out", "model", "company"):
            value = getattr(record, attr, None)
            if value is not None:
                payload[attr] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


_CONFIGURED = False


def get_logger(name: str = "aria_pi", log_dir: str | Path | None = None,
               level: str = "INFO") -> logging.Logger:
    """Return a configured logger. Idempotent — safe to call repeatedly."""
    global _CONFIGURED
    logger = logging.getLogger(name)

    if not _CONFIGURED:
        logger.setLevel(level)
        logger.handlers.clear()

        stream = logging.StreamHandler(sys.stderr)
        stream.setFormatter(JsonFormatter())
        logger.addHandler(stream)

        if log_dir is not None:
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)
            fname = datetime.utcnow().strftime("aria_pi_%Y%m%d_%H%M%S.log")
            file_handler = logging.FileHandler(log_path / fname)
            file_handler.setFormatter(JsonFormatter())
            logger.addHandler(file_handler)

        _CONFIGURED = True

    return logger
