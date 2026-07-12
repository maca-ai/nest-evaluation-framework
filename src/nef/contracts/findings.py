"""Candidate finding and human disposition contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from nef.contracts.base import ContractModel, NonEmptyString, Sha256, UtcTimestamp
from nef.contracts.canonical import canonical_sha256

type FindingSource = Literal["deterministic", "model-supported", "model-suspected"]
type FindingSeverity = Literal["critical", "high", "medium", "low", "informational"]
type DispositionDecision = Literal[
    "confirmed", "rejected", "needs-more-evidence", "accepted-risk", "fixed"
]


def finding_fingerprint(
    *, source: FindingSource, title: str, claim: str, severity: FindingSeverity
) -> str:
    """Build a stable fingerprint that deliberately excludes run/attempt identity."""
    return canonical_sha256(
        {
            "schema_version": "1.0.0",
            "source": source,
            "title": title,
            "claim": claim,
            "severity": severity,
        }
    )


class Finding(ContractModel):
    schema_version: Literal["1.0.0"]
    fingerprint: Sha256
    authority: Literal["candidate"]
    source: FindingSource
    title: NonEmptyString
    claim: NonEmptyString
    severity: FindingSeverity
    evidence_digests: tuple[Sha256, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )
    first_seen_run_id: NonEmptyString
    last_seen_run_id: NonEmptyString

    @model_validator(mode="after")
    def _validate_fingerprint(self) -> Finding:
        expected = finding_fingerprint(
            source=self.source,
            title=self.title,
            claim=self.claim,
            severity=self.severity,
        )
        if self.fingerprint != expected:
            raise ValueError("finding fingerprint mismatch")
        if len(set(self.evidence_digests)) != len(self.evidence_digests):
            raise ValueError("finding evidence digests must be unique")
        return self


class Disposition(ContractModel):
    schema_version: Literal["1.0.0"]
    finding_fingerprint: Sha256
    decision: DispositionDecision
    actor: NonEmptyString
    decided_at: UtcTimestamp
    rationale: NonEmptyString
    evidence_digests: tuple[Sha256, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )
    run_ids: tuple[NonEmptyString, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )

    @model_validator(mode="after")
    def _validate_unique_references(self) -> Disposition:
        if len(set(self.evidence_digests)) != len(self.evidence_digests):
            raise ValueError("disposition evidence digests must be unique")
        if len(set(self.run_ids)) != len(self.run_ids):
            raise ValueError("disposition run IDs must be unique")
        return self
