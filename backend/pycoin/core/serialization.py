"""Canonical serialization helpers for PyCoin."""

import json
from typing import Any


def canonical_json_bytes(data: dict[str, Any]) -> bytes:
    """Serialize a dictionary into deterministic UTF-8 JSON bytes."""
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    try:
        serialized = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("data must contain JSON-compatible values") from exc

    return serialized.encode("utf-8")
