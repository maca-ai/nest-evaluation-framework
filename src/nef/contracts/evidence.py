"""Sealed evidence manifest contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import AfterValidator, Field, StrictInt, WithJsonSchema, model_validator

from nef.contracts.base import (
    ContractModel,
    NonEmptyString,
    Sha1,
    Sha256,
    StableId,
    UtcTimestamp,
)


def _validate_evidence_path(value: str) -> str:
    if value.startswith("/") or any(segment == ".." for segment in value.split("/")):
        raise ValueError("evidence path must be relative and traversal-free")
    return value


EvidencePath = Annotated[
    str,
    AfterValidator(_validate_evidence_path),
    WithJsonSchema(
        {
            "type": "string",
            "minLength": 1,
            "pattern": r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$)).+$",
        },
        mode="validation",
    ),
]


class EvidenceProducer(ContractModel):
    nef_sha: Sha1
    tool_versions: Mapping[str, NonEmptyString]


class EvidenceObject(ContractModel):
    path: EvidencePath
    media_type: NonEmptyString
    size_bytes: StrictInt = Field(ge=0)
    sha256: Sha256


class EvidenceManifest(ContractModel):
    schema_version: Literal["1.0.0"]
    run_id: NonEmptyString
    campaign_id: StableId
    target_sha: Sha1
    protocol_digest: Sha256
    configuration_digest: Sha256
    environment_digest: Sha256
    producer: EvidenceProducer
    objects: tuple[EvidenceObject, ...] = Field(min_length=1)
    sealed_at: UtcTimestamp

    @model_validator(mode="after")
    def _validate_unique_paths(self) -> EvidenceManifest:
        paths = [item.path for item in self.objects]
        if len(set(paths)) != len(paths):
            raise ValueError("evidence object paths must be unique")
        return self
