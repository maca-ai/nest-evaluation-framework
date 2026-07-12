"""Shared validation primitives for immutable NEF contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime
from types import MappingProxyType
from typing import Annotated
from urllib.parse import urlsplit

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    StringConstraints,
    WithJsonSchema,
    model_serializer,
    model_validator,
)

SHA1_PATTERN = r"^[0-9a-f]{40}$"
SHA256_PATTERN = r"^[0-9a-f]{64}$"
STABLE_ID_PATTERN = r"^[a-z0-9]+(?:[/-][a-z0-9]+)*$"
DECIMAL_PATTERN = r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$"
GATE_TAG_PATTERN = r"^m(0|[1-9][0-9]*)$"
SEMVER_PATTERN = r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"


def _validate_utc_timestamp(value: str) -> str:
    if not value.endswith("Z"):
        raise ValueError("timestamp must be UTC with a Z suffix")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("timestamp must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise ValueError("timestamp must be UTC")
    return value


def _validate_repository_url(value: str) -> str:
    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("repository_url must be an absolute URI")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("repository_url must not contain credentials")
    return value


def _validate_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date must be ISO 8601") from exc
    if parsed.isoformat() != value:
        raise ValueError("date must use YYYY-MM-DD")
    return value


Sha1 = Annotated[str, StringConstraints(pattern=SHA1_PATTERN)]
Sha256 = Annotated[str, StringConstraints(pattern=SHA256_PATTERN)]
StableId = Annotated[str, StringConstraints(pattern=STABLE_ID_PATTERN)]
DecimalString = Annotated[str, StringConstraints(pattern=DECIMAL_PATTERN)]
GateTag = Annotated[str, StringConstraints(pattern=GATE_TAG_PATTERN)]
SemVer = Annotated[str, StringConstraints(pattern=SEMVER_PATTERN)]
NonEmptyString = Annotated[str, StringConstraints(min_length=1)]
UtcTimestamp = Annotated[
    str,
    AfterValidator(_validate_utc_timestamp),
    WithJsonSchema({"type": "string", "format": "date-time"}, mode="validation"),
]
DateString = Annotated[
    str,
    AfterValidator(_validate_date),
    WithJsonSchema({"type": "string", "format": "date"}, mode="validation"),
]
RepositoryUrl = Annotated[
    str,
    AfterValidator(_validate_repository_url),
    WithJsonSchema(
        {
            "type": "string",
            "format": "uri",
            "minLength": 1,
            "pattern": r"^(?![^:]+://[^/@]+@).+$",
        },
        mode="validation",
    ),
]


class ContractModel(BaseModel):
    """Base interface for closed, immutable contract models."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    @model_validator(mode="after")
    def _freeze_nested_values(self) -> ContractModel:
        for field_name in type(self).model_fields:
            object.__setattr__(self, field_name, _freeze(getattr(self, field_name)))
        return self

    @model_serializer(mode="plain")
    def _serialize_contract(self) -> dict[str, object]:
        return {
            field_name: _thaw(getattr(self, field_name)) for field_name in type(self).model_fields
        }


def _freeze(value: object) -> object:
    if isinstance(value, ContractModel):
        return value
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, ContractModel):
        return value._serialize_contract()  # noqa: SLF001 - shared contract implementation
    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [_thaw(item) for item in value]
    return value
