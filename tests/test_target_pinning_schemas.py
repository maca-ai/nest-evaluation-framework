from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from jsonschema.exceptions import ValidationError  # type: ignore[import-untyped]
from referencing import Registry, Resource

CONTRACTS = Path("specs/001-framework-contracts/contracts")
SHA_A = "a" * 40
SHA_B = "b" * 40
SHA256_A = "a" * 64


def load_schema(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTRACTS / name).read_text(encoding="utf-8")))


def validator(name: str) -> Draft202012Validator:
    registry = Registry()
    for path in CONTRACTS.glob("*.json"):
        contents = load_schema(path.name)
        registry = registry.with_resource(contents["$id"], Resource.from_contents(contents))
    return Draft202012Validator(load_schema(name), registry=registry)


def environment() -> dict[str, Any]:
    return {
        "digest": SHA256_A,
        "runner": "local-codex",
        "operating_system": "macOS 14.6",
        "architecture": "arm64",
        "locale": "C.UTF-8",
        "timezone": "Europe/Vienna",
        "tool_versions": {"python": "3.12.13"},
    }


def provisional_snapshot() -> dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "provisional",
        "selector": {
            "kind": "pinned-sha",
            "pinned_sha": SHA_A,
            "provisional_acknowledged": True,
        },
        "resolved_sha": SHA_A,
        "evidence_class": "non-gate-evidence",
        "baseline_reproducibility": "non-reproducible-baseline",
        "tag_binding": None,
        "dirty": False,
        "nef_sha": SHA_B,
        "lock_digest": SHA256_A,
        "constitution_version": "1.3.0",
        "constitution_digest": SHA256_A,
        "protocol_digest": SHA256_A,
        "relevant_source_digests": {"specs/001/spec.md": SHA256_A},
        "environment_fingerprint": environment(),
        "consulted_paths": ["AGENTS.md"],
        "observed_at": "2026-07-12T07:31:38Z",
    }


def gate_snapshot(
    *,
    gate_tag: str = "m0",
    tag_ref_sha: str = SHA_A,
    resolved_sha: str = SHA_B,
    binding_state: str = "first-seen",
) -> dict[str, Any]:
    prior = binding_state != "first-seen"
    return {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "gate-evidence",
        "selector": {
            "kind": "gate-tag",
            "gate_tag": gate_tag,
            "tag_ref_sha": tag_ref_sha,
        },
        "resolved_sha": resolved_sha,
        "evidence_class": "gate-evidence",
        "baseline_reproducibility": "reproducible-baseline",
        "tag_binding": {
            "state": binding_state,
            "previous_snapshot_manifest_digest": SHA256_A if prior else None,
            "previous_tag_ref_sha": SHA_B if prior else None,
            "previous_resolved_sha": SHA_A if prior else None,
        },
        "dirty": False,
        "nef_sha": SHA_A,
        "lock_digest": SHA256_A,
        "constitution_version": "1.3.0",
        "constitution_digest": SHA256_A,
        "protocol_digest": SHA256_A,
        "relevant_source_digests": {"specs/001/spec.md": SHA256_A},
        "environment_fingerprint": environment(),
        "consulted_paths": ["AGENTS.md"],
        "observed_at": "2026-07-12T07:31:38Z",
    }


def capability_manifest(*, target_sha: str = SHA_B) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "target_sha": target_sha,
        "protocol_digest": SHA256_A,
        "capabilities": [
            {
                "capability_id": "target-binding",
                "state": "available",
                "evidence": ["validated tag binding"],
                "reason": None,
            }
        ],
        "required_campaigns": ["target-integrity/target-binding"],
        "unavailable_campaigns_with_reasons": [],
        "observed_at": "2026-07-12T07:31:38Z",
    }


def campaign_request(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "run_id": "2026-07-12/bbbbbbbb/aaaaaaaa",
        "scheduled_date": "2026-07-12",
        "attempt": 1,
        "campaign_id": "target-integrity/target-binding",
        "target_snapshot_manifest": snapshot,
        "target_snapshot_manifest_digest": SHA256_A,
        "target_capability_manifest": capability_manifest(target_sha=snapshot["resolved_sha"]),
        "target_capability_manifest_digest": SHA256_A,
        "campaign_configuration_digest": SHA256_A,
        "budgets": {
            "timeout_seconds": 60,
            "max_cost_eur": "0",
            "max_memory_mib": 128,
            "max_output_bytes": 100000,
        },
        "disposable_workspace": f".targets/nest/{snapshot['resolved_sha']}",
        "randomness": {"mode": "not-applicable", "seed": None},
    }


def test_provisional_descriptor_records_only_an_explicit_pinned_sha() -> None:
    descriptor = {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "provisional",
        "selector": {
            "kind": "pinned-sha",
            "pinned_sha": SHA_A,
            "provisional_acknowledged": True,
        },
        "resolved_sha": SHA_A,
        "observed_at": "2026-07-12T07:31:38Z",
        "source_kind": "remote",
    }

    validator("target-descriptor.schema.json").validate(descriptor)


@pytest.mark.parametrize("contract_layer", ["descriptor", "snapshot"])
@pytest.mark.parametrize("acknowledgement", [False, pytest.param("absent", id="absent")])
def test_unacknowledged_provisional_selector_is_rejected(
    contract_layer: str, acknowledgement: bool | str
) -> None:
    instance: dict[str, Any]
    if contract_layer == "descriptor":
        instance = {
            "schema_version": "2.0.0",
            "repository_url": "https://github.com/maca-ai/nest.git",
            "target_mode": "provisional",
            "selector": {
                "kind": "pinned-sha",
                "pinned_sha": SHA_A,
                "provisional_acknowledged": True,
            },
            "resolved_sha": SHA_A,
            "observed_at": "2026-07-12T07:31:38Z",
            "source_kind": "remote",
        }
        schema_name = "target-descriptor.schema.json"
    else:
        instance = provisional_snapshot()
        schema_name = "target-snapshot-manifest.schema.json"

    if acknowledgement == "absent":
        instance["selector"].pop("provisional_acknowledged")
    else:
        instance["selector"]["provisional_acknowledged"] = acknowledgement

    with pytest.raises(ValidationError):
        validator(schema_name).validate(instance)


@pytest.mark.parametrize("mutable_ref", ["main", "HEAD", "refs/heads/main", "latest"])
def test_mutable_ref_cannot_be_a_recorded_campaign_selector(mutable_ref: str) -> None:
    descriptor = {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "gate-evidence",
        "selector": {"kind": "branch", "ref": mutable_ref},
        "resolved_sha": SHA_A,
        "observed_at": "2026-07-12T07:31:38Z",
        "source_kind": "remote",
    }

    with pytest.raises(ValidationError):
        validator("target-descriptor.schema.json").validate(descriptor)


@pytest.mark.parametrize(
    ("gate_tag", "tag_ref_sha", "resolved_sha"),
    [
        ("m0", SHA_A, SHA_B),  # annotated: peeling dereferences the tag object
        ("m1", SHA_A, SHA_A),  # lightweight: peeling a commit is the identity
    ],
)
def test_gate_descriptor_supports_annotated_and_lightweight_tags(
    gate_tag: str, tag_ref_sha: str, resolved_sha: str
) -> None:
    descriptor = {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "gate-evidence",
        "selector": {
            "kind": "gate-tag",
            "gate_tag": gate_tag,
            "tag_ref_sha": tag_ref_sha,
        },
        "resolved_sha": resolved_sha,
        "observed_at": "2026-07-12T07:31:38Z",
        "source_kind": "remote",
    }

    validator("target-descriptor.schema.json").validate(descriptor)


def test_provisional_snapshot_is_explicitly_non_gate_non_baseline_evidence() -> None:
    validator("target-snapshot-manifest.schema.json").validate(provisional_snapshot())


@pytest.mark.parametrize(
    ("gate_tag", "tag_ref_sha", "resolved_sha"),
    [("m0", SHA_A, SHA_B), ("m1", SHA_A, SHA_A)],
)
def test_gate_snapshot_records_annotated_or_lightweight_binding(
    gate_tag: str, tag_ref_sha: str, resolved_sha: str
) -> None:
    validator("target-snapshot-manifest.schema.json").validate(
        gate_snapshot(gate_tag=gate_tag, tag_ref_sha=tag_ref_sha, resolved_sha=resolved_sha)
    )


def test_mode_and_evidence_class_cannot_disagree() -> None:
    snapshot = provisional_snapshot()
    snapshot["evidence_class"] = "gate-evidence"

    with pytest.raises(ValidationError):
        validator("target-snapshot-manifest.schema.json").validate(snapshot)


def test_moved_tag_snapshot_is_valid_violation_evidence() -> None:
    validator("target-snapshot-manifest.schema.json").validate(gate_snapshot(binding_state="moved"))


def test_unchanged_gate_binding_is_executable_campaign_input() -> None:
    validator("campaign-request.schema.json").validate(
        campaign_request(gate_snapshot(binding_state="unchanged"))
    )


def test_moved_gate_binding_is_never_executable_campaign_input() -> None:
    with pytest.raises(ValidationError):
        validator("campaign-request.schema.json").validate(
            campaign_request(gate_snapshot(binding_state="moved"))
        )


def test_provisional_binding_is_executable_but_remains_non_gate_evidence() -> None:
    validator("campaign-request.schema.json").validate(campaign_request(provisional_snapshot()))


def test_moved_binding_requires_prior_snapshot_evidence() -> None:
    snapshot = gate_snapshot(binding_state="moved")
    snapshot["tag_binding"]["previous_snapshot_manifest_digest"] = None

    with pytest.raises(ValidationError):
        validator("target-snapshot-manifest.schema.json").validate(snapshot)


def test_normative_contracts_are_valid_draft_2020_12_schemas() -> None:
    for path in CONTRACTS.glob("*.json"):
        Draft202012Validator.check_schema(load_schema(path.name))
