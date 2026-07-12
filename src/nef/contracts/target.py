"""Target selection and pinning contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import ConfigDict, Field, StrictBool, ValidationInfo, model_validator

from nef.contracts.base import (
    ContractModel,
    GateTag,
    NonEmptyString,
    RepositoryUrl,
    SemVer,
    Sha1,
    Sha256,
    StableId,
    UtcTimestamp,
)


class GateSelector(ContractModel):
    kind: Literal["gate-tag"]
    gate_tag: GateTag
    tag_ref_sha: Sha1


class ProvisionalSelector(ContractModel):
    kind: Literal["pinned-sha"]
    pinned_sha: Sha1
    provisional_acknowledged: Literal[True]


TargetSelector = Annotated[GateSelector | ProvisionalSelector, Field(discriminator="kind")]


def _require_verified_peel(selector: GateSelector, resolved_sha: str, info: ValidationInfo) -> None:
    if selector.tag_ref_sha == resolved_sha:
        return
    context = info.context
    if not isinstance(context, Mapping):
        raise ValueError("annotated gate tag requires verified peel evidence")
    bindings = context.get("peel_bindings")
    if not isinstance(bindings, Mapping) or selector.tag_ref_sha not in bindings:
        raise ValueError("annotated gate tag requires verified peel evidence")
    if bindings[selector.tag_ref_sha] != resolved_sha:
        raise ValueError("verified peel does not equal resolved_sha")


class TargetDescriptor(ContractModel):
    schema_version: Literal["2.0.0"]
    repository_url: RepositoryUrl
    target_mode: Literal["gate-evidence", "provisional"]
    selector: TargetSelector
    resolved_sha: Sha1
    observed_at: UtcTimestamp
    source_kind: Literal["local", "remote"]

    @model_validator(mode="after")
    def _validate_selector_coherence(self, info: ValidationInfo) -> TargetDescriptor:
        if self.target_mode == "provisional":
            if not isinstance(self.selector, ProvisionalSelector):
                raise ValueError("provisional target_mode requires a pinned-sha selector")
            if self.selector.pinned_sha != self.resolved_sha:
                raise ValueError("pinned_sha must equal resolved_sha")
            return self

        if not isinstance(self.selector, GateSelector):
            raise ValueError("gate-evidence target_mode requires a gate-tag selector")
        _require_verified_peel(self.selector, self.resolved_sha, info)
        return self


class UnavailableNefSha(ContractModel):
    unavailable_reason: NonEmptyString


class TagBinding(ContractModel):
    model_config = ConfigDict(
        json_schema_extra={
            "allOf": [
                {
                    "if": {"properties": {"state": {"const": "first-seen"}}, "required": ["state"]},
                    "then": {
                        "properties": {
                            "previous_snapshot_manifest_digest": {"type": "null"},
                            "previous_tag_ref_sha": {"type": "null"},
                            "previous_resolved_sha": {"type": "null"},
                        }
                    },
                    "else": {
                        "properties": {
                            "previous_snapshot_manifest_digest": {
                                "type": "string",
                                "pattern": r"^[0-9a-f]{64}$",
                            },
                            "previous_tag_ref_sha": {
                                "type": "string",
                                "pattern": r"^[0-9a-f]{40}$",
                            },
                            "previous_resolved_sha": {
                                "type": "string",
                                "pattern": r"^[0-9a-f]{40}$",
                            },
                        }
                    },
                }
            ]
        }
    )

    state: Literal["first-seen", "unchanged", "moved"]
    previous_snapshot_manifest_digest: Sha256 | None
    previous_tag_ref_sha: Sha1 | None
    previous_resolved_sha: Sha1 | None

    @model_validator(mode="after")
    def _validate_previous_binding(self) -> TagBinding:
        previous = (
            self.previous_snapshot_manifest_digest,
            self.previous_tag_ref_sha,
            self.previous_resolved_sha,
        )
        if self.state == "first-seen" and any(value is not None for value in previous):
            raise ValueError("first-seen binding must not include previous evidence")
        if self.state != "first-seen" and any(value is None for value in previous):
            raise ValueError("unchanged or moved binding requires complete previous evidence")
        return self


class EnvironmentFingerprint(ContractModel):
    digest: Sha256
    runner: NonEmptyString
    operating_system: NonEmptyString
    architecture: NonEmptyString
    locale: NonEmptyString
    timezone: NonEmptyString
    tool_versions: Mapping[str, NonEmptyString] = Field(default_factory=dict)


class TargetSnapshotManifest(ContractModel):
    schema_version: Literal["2.0.0"]
    repository_url: RepositoryUrl
    target_mode: Literal["gate-evidence", "provisional"]
    selector: TargetSelector
    resolved_sha: Sha1
    evidence_class: Literal["gate-evidence", "non-gate-evidence"]
    baseline_reproducibility: Literal["reproducible-baseline", "non-reproducible-baseline"]
    tag_binding: TagBinding | None
    dirty: StrictBool
    nef_sha: Sha1 | UnavailableNefSha
    lock_digest: Sha256
    constitution_version: SemVer
    constitution_digest: Sha256
    protocol_digest: Sha256
    relevant_source_digests: Mapping[NonEmptyString, Sha256] = Field(min_length=1)
    environment_fingerprint: EnvironmentFingerprint
    consulted_paths: tuple[NonEmptyString, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )
    observed_at: UtcTimestamp

    @model_validator(mode="after")
    def _validate_snapshot_coherence(self, info: ValidationInfo) -> TargetSnapshotManifest:
        if len(set(self.consulted_paths)) != len(self.consulted_paths):
            raise ValueError("consulted_paths must be unique")
        if self.target_mode == "provisional":
            if not isinstance(self.selector, ProvisionalSelector):
                raise ValueError("provisional target_mode requires a pinned-sha selector")
            if self.selector.pinned_sha != self.resolved_sha:
                raise ValueError("pinned_sha must equal resolved_sha")
            if self.evidence_class != "non-gate-evidence":
                raise ValueError("provisional targets must be non-gate-evidence")
            if self.baseline_reproducibility != "non-reproducible-baseline":
                raise ValueError("provisional targets must be non-reproducible-baseline")
            if self.tag_binding is not None:
                raise ValueError("provisional targets must not have a tag binding")
            return self

        if not isinstance(self.selector, GateSelector):
            raise ValueError("gate-evidence target_mode requires a gate-tag selector")
        if self.evidence_class != "gate-evidence":
            raise ValueError("gate targets must be gate-evidence")
        if self.baseline_reproducibility != "reproducible-baseline":
            raise ValueError("gate targets must be reproducible-baseline")
        if self.tag_binding is None:
            raise ValueError("gate targets require a tag binding")
        _require_verified_peel(self.selector, self.resolved_sha, info)
        if self.tag_binding.state == "unchanged" and (
            self.tag_binding.previous_tag_ref_sha != self.selector.tag_ref_sha
            or self.tag_binding.previous_resolved_sha != self.resolved_sha
        ):
            raise ValueError("unchanged tag binding must match current binding")
        if (
            self.tag_binding.state == "moved"
            and self.tag_binding.previous_tag_ref_sha == self.selector.tag_ref_sha
            and self.tag_binding.previous_resolved_sha == self.resolved_sha
        ):
            raise ValueError("moved tag binding must differ from current binding")
        return self


class Capability(ContractModel):
    model_config = ConfigDict(
        json_schema_extra={
            "allOf": [
                {
                    "if": {
                        "properties": {"state": {"const": "unavailable"}},
                        "required": ["state"],
                    },
                    "then": {
                        "required": ["reason"],
                        "properties": {"reason": {"type": "string", "minLength": 1}},
                    },
                }
            ]
        }
    )

    capability_id: StableId
    state: Literal["available", "unavailable"]
    evidence: tuple[NonEmptyString, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )
    reason: NonEmptyString | None = None

    @model_validator(mode="after")
    def _validate_reason(self) -> Capability:
        if self.state == "unavailable" and self.reason is None:
            raise ValueError("unavailable capability requires a reason")
        if len(set(self.evidence)) != len(self.evidence):
            raise ValueError("capability evidence must be unique")
        return self


class UnavailableCampaign(ContractModel):
    campaign_id: StableId
    state: Literal["skipped"]
    reason: NonEmptyString
    missing_evidence: tuple[NonEmptyString, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )

    @model_validator(mode="after")
    def _validate_missing_evidence(self) -> UnavailableCampaign:
        if len(set(self.missing_evidence)) != len(self.missing_evidence):
            raise ValueError("missing_evidence must be unique")
        return self


class TargetCapabilityManifest(ContractModel):
    schema_version: Literal["1.0.0"]
    target_sha: Sha1
    protocol_digest: Sha256
    capabilities: tuple[Capability, ...] = Field(min_length=1)
    required_campaigns: tuple[StableId, ...] = Field(
        min_length=1, json_schema_extra={"uniqueItems": True}
    )
    unavailable_campaigns_with_reasons: tuple[UnavailableCampaign, ...]
    observed_at: UtcTimestamp

    @model_validator(mode="after")
    def _validate_unique_ids(self) -> TargetCapabilityManifest:
        capability_ids = [capability.capability_id for capability in self.capabilities]
        unavailable_ids = [
            campaign.campaign_id for campaign in self.unavailable_campaigns_with_reasons
        ]
        if len(set(capability_ids)) != len(capability_ids):
            raise ValueError("capability IDs must be unique")
        if len(set(self.required_campaigns)) != len(self.required_campaigns):
            raise ValueError("required campaign IDs must be unique")
        if len(set(unavailable_ids)) != len(unavailable_ids):
            raise ValueError("unavailable campaign IDs must be unique")
        return self
