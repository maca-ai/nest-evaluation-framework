"""Campaign request, result, case, replay, and budget contracts."""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    Field,
    StrictBool,
    StrictInt,
    WithJsonSchema,
    model_validator,
)

from nef.contracts.base import (
    ContractModel,
    DateString,
    DecimalString,
    NonEmptyString,
    Sha256,
    StableId,
    UtcTimestamp,
)
from nef.contracts.canonical import canonical_json_bytes, canonical_sha256
from nef.contracts.target import TargetCapabilityManifest, TargetSnapshotManifest

type EvaluationState = Literal["pass", "fail", "error", "inconclusive", "invalid", "skipped"]
type CanonicalValue = (
    None | StrictBool | StrictInt | str | list[CanonicalValue] | dict[str, CanonicalValue]
)
type MeasurementValue = StrictInt | str | StrictBool


def _validate_workspace(value: str) -> str:
    if re.fullmatch(r"\.targets/nest/[0-9a-f]{40}(?:/[^/]+)*", value) is None:
        raise ValueError("invalid disposable workspace")
    if any(segment in {".", ".."} for segment in value.split("/")[3:]):
        raise ValueError("disposable workspace must not traverse directories")
    return value


WorkspacePath = Annotated[
    str,
    AfterValidator(_validate_workspace),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^\.targets/nest/[0-9a-f]{40}(?:/(?!\.{1,2}(?:/|$))[^/]+)*$",
        },
        mode="validation",
    ),
]


def run_id_for(scheduled_date: str, target_sha: str, protocol_digest: str) -> str:
    """Build the one canonical run identity independent of rerun attempt."""
    return f"{scheduled_date}/{target_sha}/{protocol_digest}"


def _nonnegative_decimal(value: str, *, field_name: str) -> None:
    if Decimal(value) < 0:
        raise ValueError(f"{field_name} must be non-negative")


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


class CampaignBudgets(ContractModel):
    timeout_seconds: StrictInt = Field(ge=1)
    max_cost_eur: DecimalString
    max_memory_mib: StrictInt = Field(ge=1)
    max_output_bytes: StrictInt = Field(ge=1)

    @model_validator(mode="after")
    def _validate_cost(self) -> CampaignBudgets:
        _nonnegative_decimal(self.max_cost_eur, field_name="max_cost_eur")
        return self


class Randomness(ContractModel):
    mode: Literal["not-applicable", "recorded"]
    seed: StrictInt | None = None
    supplemental_reproduction_data: str | None = None

    @model_validator(mode="after")
    def _validate_mode(self) -> Randomness:
        if self.mode == "recorded" and self.seed is None:
            raise ValueError("recorded randomness requires a seed")
        if self.mode == "not-applicable" and (
            self.seed is not None or self.supplemental_reproduction_data is not None
        ):
            raise ValueError("not-applicable randomness cannot carry reproduction data")
        return self


class CampaignRequest(ContractModel):
    schema_version: Literal["2.0.0"]
    run_id: NonEmptyString
    scheduled_date: DateString
    attempt: StrictInt = Field(ge=1)
    campaign_id: StableId
    target_snapshot_manifest: TargetSnapshotManifest
    target_snapshot_manifest_digest: Sha256
    target_capability_manifest: TargetCapabilityManifest
    target_capability_manifest_digest: Sha256
    campaign_configuration_digest: Sha256
    budgets: CampaignBudgets
    disposable_workspace: WorkspacePath
    randomness: Randomness

    @model_validator(mode="after")
    def _validate_request_coherence(self) -> CampaignRequest:
        snapshot = self.target_snapshot_manifest
        capabilities = self.target_capability_manifest
        if snapshot.tag_binding is not None and snapshot.tag_binding.state == "moved":
            raise ValueError("moved target binding cannot execute")
        if capabilities.target_sha != snapshot.resolved_sha:
            raise ValueError("target capability SHA does not equal snapshot SHA")
        if capabilities.protocol_digest != snapshot.protocol_digest:
            raise ValueError("target capability protocol does not equal snapshot protocol")
        if canonical_sha256(snapshot) != self.target_snapshot_manifest_digest:
            raise ValueError("target snapshot manifest digest mismatch")
        if canonical_sha256(capabilities) != self.target_capability_manifest_digest:
            raise ValueError("target capability manifest digest mismatch")
        expected_run_id = run_id_for(
            self.scheduled_date, snapshot.resolved_sha, snapshot.protocol_digest
        )
        if self.run_id != expected_run_id:
            raise ValueError("run_id does not match date, target SHA, and protocol digest")
        workspace_root = f".targets/nest/{snapshot.resolved_sha}"
        if self.disposable_workspace != workspace_root and not self.disposable_workspace.startswith(
            workspace_root + "/"
        ):
            raise ValueError("disposable workspace does not match target SHA")
        if self.campaign_id not in capabilities.required_campaigns:
            raise ValueError("campaign is not required by the target capability manifest")
        return self


class CaseResult(ContractModel):
    case_id: StableId
    state: EvaluationState
    reason: str | None
    evidence_digests: tuple[Sha256, ...] = Field(json_schema_extra={"uniqueItems": True})

    @model_validator(mode="after")
    def _validate_case_evidence(self) -> CaseResult:
        if len(set(self.evidence_digests)) != len(self.evidence_digests):
            raise ValueError("case evidence digests must be unique")
        if self.state == "pass" and not self.evidence_digests:
            raise ValueError("pass cases require evidence")
        if self.state == "skipped" and not self.reason:
            raise ValueError("skipped cases require a reason")
        return self


class ReplayMetadata(ContractModel):
    replayable: StrictBool
    data: Mapping[str, CanonicalValue]

    @model_validator(mode="after")
    def _validate_canonical_data(self) -> ReplayMetadata:
        canonical_json_bytes(self.data)
        return self


class BudgetUse(ContractModel):
    elapsed_seconds: DecimalString
    cost_eur: DecimalString
    peak_memory_mib: StrictInt = Field(ge=0)
    output_bytes: StrictInt = Field(ge=0)

    @model_validator(mode="after")
    def _validate_decimals(self) -> BudgetUse:
        _nonnegative_decimal(self.elapsed_seconds, field_name="elapsed_seconds")
        _nonnegative_decimal(self.cost_eur, field_name="cost_eur")
        return self


class CampaignResult(ContractModel):
    schema_version: Literal["1.0.0"]
    run_id: NonEmptyString
    campaign_id: StableId
    state: EvaluationState
    required: StrictBool
    started_at: UtcTimestamp
    finished_at: UtcTimestamp
    cases: tuple[CaseResult, ...]
    measurements: Mapping[str, MeasurementValue]
    candidate_finding_fingerprints: tuple[Sha256, ...] = Field(
        json_schema_extra={"uniqueItems": True}
    )
    replay_metadata: ReplayMetadata
    budget_use: BudgetUse
    evidence_manifest_digest: Sha256 | None

    @model_validator(mode="after")
    def _validate_result(self) -> CampaignResult:
        if _timestamp(self.finished_at) < _timestamp(self.started_at):
            raise ValueError("finished_at must not precede started_at")
        case_ids = [case.case_id for case in self.cases]
        if len(set(case_ids)) != len(case_ids):
            raise ValueError("case IDs must be unique")
        if len(set(self.candidate_finding_fingerprints)) != len(
            self.candidate_finding_fingerprints
        ):
            raise ValueError("candidate finding fingerprints must be unique")
        canonical_json_bytes(self.measurements)
        if self.state == "pass":
            if self.evidence_manifest_digest is None:
                raise ValueError("pass requires an evidence manifest digest")
            if not self.cases:
                raise ValueError("pass requires at least one case")
            if any(case.state != "pass" for case in self.cases):
                raise ValueError("pass requires every case to pass")
        if self.state == "skipped":
            if not self.cases or any(case.state != "skipped" for case in self.cases):
                raise ValueError("skipped result requires skipped cases")
        return self
