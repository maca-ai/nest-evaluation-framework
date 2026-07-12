"""Canonical JSON and digest helpers shared by all contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence

from pydantic import BaseModel


def _json_value(value: object, *, path: str = "$") -> object:
    if isinstance(value, BaseModel):
        return _json_value(value.model_dump(mode="json"), path=path)
    if value is None or isinstance(value, bool | int | str):
        return value
    if isinstance(value, float):
        raise TypeError(f"floats are forbidden in canonical data at {path}")
    if isinstance(value, Mapping):
        result: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"canonical object keys must be strings at {path}")
            result[key] = _json_value(item, path=f"{path}.{key}")
        return result
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [_json_value(item, path=f"{path}[{index}]") for index, item in enumerate(value)]
    raise TypeError(f"unsupported canonical value {type(value).__name__} at {path}")


def canonical_json_bytes(value: object) -> bytes:
    """Return compact UTF-8 sorted-key JSON and reject non-canonical values."""
    normalized = _json_value(value)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: object) -> str:
    """Digest a value only after canonical validation and serialization."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def canonical_json_text(value: object) -> str:
    """Return canonical JSON as text for CLI output."""
    return canonical_json_bytes(value).decode("utf-8")
