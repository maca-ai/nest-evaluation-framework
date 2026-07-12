from __future__ import annotations

from copy import deepcopy
from typing import Any, cast

import pytest
from pydantic import ValidationError

from nef.contracts import (
    CampaignRequest,
    CampaignResult,
    Disposition,
    EvidenceManifest,
    Finding,
    ProvisionalSelector,
    TargetCapabilityManifest,
    TargetDescriptor,
    TargetSnapshotManifest,
    canonical_json_bytes,
    canonical_sha256,
    finding_fingerprint,
    run_id_for,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA256_A = "a" * 64


def provisional_descriptor(
    *, pinned_sha: str = SHA_A, resolved_sha: str = SHA_A
) -> dict[str, object]:
    return {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "provisional",
        "selector": {
            "kind": "pinned-sha",
            "pinned_sha": pinned_sha,
            "provisional_acknowledged": True,
        },
        "resolved_sha": resolved_sha,
        "observed_at": "2026-07-12T13:05:01Z",
        "source_kind": "remote",
    }


def test_provisional_descriptor_requires_pinned_sha_to_equal_resolved_sha() -> None:
    descriptor = TargetDescriptor.model_validate(provisional_descriptor())
    assert descriptor.resolved_sha == SHA_A

    with pytest.raises(ValidationError, match="pinned_sha must equal resolved_sha"):
        TargetDescriptor.model_validate(provisional_descriptor(resolved_sha=SHA_B))


def gate_descriptor(*, tag_ref_sha: str = SHA_A, resolved_sha: str = SHA_B) -> dict[str, object]:
    return {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "gate-evidence",
        "selector": {
            "kind": "gate-tag",
            "gate_tag": "m0",
            "tag_ref_sha": tag_ref_sha,
        },
        "resolved_sha": resolved_sha,
        "observed_at": "2026-07-12T13:05:01Z",
        "source_kind": "remote",
    }


def test_gate_descriptor_requires_verified_peel_or_lightweight_identity() -> None:
    lightweight = TargetDescriptor.model_validate(
        gate_descriptor(tag_ref_sha=SHA_A, resolved_sha=SHA_A)
    )
    assert lightweight.resolved_sha == SHA_A

    annotated = TargetDescriptor.model_validate(
        gate_descriptor(), context={"peel_bindings": {SHA_A: SHA_B}}
    )
    assert annotated.resolved_sha == SHA_B

    with pytest.raises(ValidationError, match="annotated gate tag requires verified peel evidence"):
        TargetDescriptor.model_validate(gate_descriptor())

    with pytest.raises(ValidationError, match="verified peel does not equal resolved_sha"):
        TargetDescriptor.model_validate(
            gate_descriptor(), context={"peel_bindings": {SHA_A: "c" * 40}}
        )


def test_contracts_are_closed_frozen_and_canonical_json_rejects_floats() -> None:
    descriptor = TargetDescriptor.model_validate(provisional_descriptor())

    with pytest.raises(ValidationError, match="Instance is frozen"):
        descriptor.resolved_sha = SHA_B
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        TargetDescriptor.model_validate({**provisional_descriptor(), "unexpected": True})

    assert canonical_json_bytes({"z": 1, "a": [True, None, "x"]}) == (
        b'{"a":[true,null,"x"],"z":1}'
    )
    assert canonical_sha256({"z": 1, "a": [True, None, "x"]}) == (
        "cc31fc728ab32ccfd6543dd8cce686b9633b3c47fbec82c88a466688f3a8cb81"
    )
    with pytest.raises(TypeError, match="floats are forbidden"):
        canonical_json_bytes({"measurement": 1.5})


def provisional_snapshot(
    *, pinned_sha: str = SHA_A, resolved_sha: str = SHA_A
) -> dict[str, object]:
    return {
        "schema_version": "2.0.0",
        "repository_url": "https://github.com/maca-ai/nest.git",
        "target_mode": "provisional",
        "selector": {
            "kind": "pinned-sha",
            "pinned_sha": pinned_sha,
            "provisional_acknowledged": True,
        },
        "resolved_sha": resolved_sha,
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
        "environment_fingerprint": {
            "digest": SHA256_A,
            "runner": "pytest",
            "operating_system": "test-os",
            "architecture": "arm64",
            "locale": "C.UTF-8",
            "timezone": "UTC",
            "tool_versions": {"python": "3.12.13"},
        },
        "consulted_paths": ["AGENTS.md"],
        "observed_at": "2026-07-12T13:05:01Z",
    }


def test_target_snapshot_enforces_mode_coherence_and_deep_immutability() -> None:
    snapshot = TargetSnapshotManifest.model_validate(provisional_snapshot())
    assert isinstance(snapshot.selector, ProvisionalSelector)
    assert snapshot.selector.pinned_sha == SHA_A
    assert snapshot.consulted_paths == ("AGENTS.md",)

    with pytest.raises(ValidationError, match="pinned_sha must equal resolved_sha"):
        TargetSnapshotManifest.model_validate(provisional_snapshot(resolved_sha=SHA_B))
    with pytest.raises(TypeError):
        snapshot.relevant_source_digests["other"] = SHA256_A  # type: ignore[index]
    with pytest.raises(TypeError):
        snapshot.environment_fingerprint.tool_versions["python"] = "changed"  # type: ignore[index]


def test_target_capability_manifest_keeps_unavailable_campaigns_explicit() -> None:
    manifest = TargetCapabilityManifest.model_validate(
        {
            "schema_version": "1.0.0",
            "target_sha": SHA_A,
            "protocol_digest": SHA256_A,
            "capabilities": [
                {
                    "capability_id": "target-binding",
                    "state": "available",
                    "evidence": ["validated binding"],
                    "reason": None,
                }
            ],
            "required_campaigns": ["target-integrity/target-binding"],
            "unavailable_campaigns_with_reasons": [
                {
                    "campaign_id": "target-integrity/ed25519",
                    "state": "skipped",
                    "reason": "ratified protocol unavailable",
                    "missing_evidence": ["signing fixture"],
                }
            ],
            "observed_at": "2026-07-12T13:05:01Z",
        }
    )
    assert manifest.required_campaigns == ("target-integrity/target-binding",)


def capability_manifest() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "target_sha": SHA_A,
        "protocol_digest": SHA256_A,
        "capabilities": [
            {
                "capability_id": "target-binding",
                "state": "available",
                "evidence": ["validated binding"],
                "reason": None,
            }
        ],
        "required_campaigns": ["target-integrity/target-binding"],
        "unavailable_campaigns_with_reasons": [],
        "observed_at": "2026-07-12T13:05:01Z",
    }


def campaign_request() -> dict[str, object]:
    snapshot = provisional_snapshot()
    capabilities = capability_manifest()
    return {
        "schema_version": "2.0.0",
        "run_id": run_id_for("2026-07-12", SHA_A, SHA256_A),
        "scheduled_date": "2026-07-12",
        "attempt": 1,
        "campaign_id": "target-integrity/target-binding",
        "target_snapshot_manifest": snapshot,
        "target_snapshot_manifest_digest": canonical_sha256(snapshot),
        "target_capability_manifest": capabilities,
        "target_capability_manifest_digest": canonical_sha256(capabilities),
        "campaign_configuration_digest": SHA256_A,
        "budgets": {
            "timeout_seconds": 60,
            "max_cost_eur": "0",
            "max_memory_mib": 128,
            "max_output_bytes": 100_000,
        },
        "disposable_workspace": f".targets/nest/{SHA_A}",
        "randomness": {"mode": "not-applicable", "seed": None},
    }


def moved_gate_snapshot() -> dict[str, object]:
    snapshot = provisional_snapshot()
    snapshot.update(
        {
            "target_mode": "gate-evidence",
            "selector": {"kind": "gate-tag", "gate_tag": "m0", "tag_ref_sha": SHA_A},
            "resolved_sha": SHA_B,
            "evidence_class": "gate-evidence",
            "baseline_reproducibility": "reproducible-baseline",
            "tag_binding": {
                "state": "moved",
                "previous_snapshot_manifest_digest": SHA256_A,
                "previous_tag_ref_sha": SHA_A,
                "previous_resolved_sha": SHA_A,
            },
        }
    )
    return snapshot


def test_campaign_request_rejects_moved_or_incoherent_target_evidence() -> None:
    request = CampaignRequest.model_validate(campaign_request())
    assert request.run_id == run_id_for("2026-07-12", SHA_A, SHA256_A)

    wrong_digest = deepcopy(campaign_request())
    wrong_digest["target_snapshot_manifest_digest"] = "b" * 64
    with pytest.raises(ValidationError, match="target snapshot manifest digest mismatch"):
        CampaignRequest.model_validate(wrong_digest)

    moved = campaign_request()
    moved_snapshot = moved_gate_snapshot()
    moved["target_snapshot_manifest"] = moved_snapshot
    moved["target_snapshot_manifest_digest"] = canonical_sha256(moved_snapshot)
    with pytest.raises(ValidationError, match="moved target binding cannot execute"):
        CampaignRequest.model_validate(moved, context={"peel_bindings": {SHA_A: SHA_B}})


def test_campaign_request_rejects_each_identity_and_capability_mismatch() -> None:
    wrong_run = campaign_request()
    wrong_run["run_id"] = "wrong-run"
    with pytest.raises(ValidationError, match="run_id does not match"):
        CampaignRequest.model_validate(wrong_run)

    wrong_workspace = campaign_request()
    wrong_workspace["disposable_workspace"] = f".targets/nest/{SHA_B}"
    with pytest.raises(ValidationError, match="workspace does not match target SHA"):
        CampaignRequest.model_validate(wrong_workspace)

    wrong_capability_digest = campaign_request()
    wrong_capability_digest["target_capability_manifest_digest"] = "b" * 64
    with pytest.raises(ValidationError, match="capability manifest digest mismatch"):
        CampaignRequest.model_validate(wrong_capability_digest)

    wrong_target = campaign_request()
    capabilities = cast(dict[str, Any], wrong_target["target_capability_manifest"])
    capabilities["target_sha"] = SHA_B
    wrong_target["target_capability_manifest_digest"] = canonical_sha256(capabilities)
    with pytest.raises(ValidationError, match="capability SHA does not equal snapshot SHA"):
        CampaignRequest.model_validate(wrong_target)

    wrong_protocol = campaign_request()
    capabilities = cast(dict[str, Any], wrong_protocol["target_capability_manifest"])
    capabilities["protocol_digest"] = "b" * 64
    wrong_protocol["target_capability_manifest_digest"] = canonical_sha256(capabilities)
    with pytest.raises(ValidationError, match="capability protocol does not equal snapshot"):
        CampaignRequest.model_validate(wrong_protocol)

    unavailable = campaign_request()
    capabilities = cast(dict[str, Any], unavailable["target_capability_manifest"])
    capabilities["required_campaigns"] = ["target-integrity/other"]
    unavailable["target_capability_manifest_digest"] = canonical_sha256(capabilities)
    with pytest.raises(ValidationError, match="campaign is not required"):
        CampaignRequest.model_validate(unavailable)


def passing_campaign_result() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "run_id": run_id_for("2026-07-12", SHA_A, SHA256_A),
        "campaign_id": "target-integrity/target-binding",
        "state": "pass",
        "required": True,
        "started_at": "2026-07-12T13:05:01Z",
        "finished_at": "2026-07-12T13:05:02Z",
        "cases": [
            {
                "case_id": "target-binding/valid",
                "state": "pass",
                "reason": None,
                "evidence_digests": [SHA256_A],
            }
        ],
        "measurements": {"checks": 1, "ratio": "1.0", "deterministic": True},
        "candidate_finding_fingerprints": [],
        "replay_metadata": {"replayable": True, "data": {"seed": 7}},
        "budget_use": {
            "elapsed_seconds": "1.0",
            "cost_eur": "0",
            "peak_memory_mib": 1,
            "output_bytes": 100,
        },
        "evidence_manifest_digest": SHA256_A,
    }


def test_campaign_result_pass_requires_complete_sealed_evidence() -> None:
    result = CampaignResult.model_validate(passing_campaign_result())
    assert result.state == "pass"

    missing_manifest = deepcopy(passing_campaign_result())
    missing_manifest["evidence_manifest_digest"] = None
    with pytest.raises(ValidationError, match="pass requires an evidence manifest digest"):
        CampaignResult.model_validate(missing_manifest)

    missing_case_evidence = deepcopy(passing_campaign_result())
    missing_case_evidence["cases"][0]["evidence_digests"] = []  # type: ignore[index]
    with pytest.raises(ValidationError, match="pass cases require evidence"):
        CampaignResult.model_validate(missing_case_evidence)

    mixed_pass = deepcopy(passing_campaign_result())
    mixed_pass["cases"][0]["state"] = "fail"  # type: ignore[index]
    with pytest.raises(ValidationError, match="every case to pass"):
        CampaignResult.model_validate(mixed_pass)

    reversed_time = deepcopy(passing_campaign_result())
    reversed_time["finished_at"] = "2026-07-12T13:05:00Z"
    with pytest.raises(ValidationError, match="must not precede"):
        CampaignResult.model_validate(reversed_time)

    float_measurement = deepcopy(passing_campaign_result())
    float_measurement["measurements"] = {"ratio": 1.0}
    with pytest.raises(ValidationError):
        CampaignResult.model_validate(float_measurement)


def test_skipped_results_require_explicit_skipped_cases_and_reason() -> None:
    skipped = deepcopy(passing_campaign_result())
    skipped["state"] = "skipped"
    skipped["cases"][0]["state"] = "skipped"  # type: ignore[index]
    skipped["cases"][0]["reason"] = "capability unavailable"  # type: ignore[index]
    skipped["cases"][0]["evidence_digests"] = []  # type: ignore[index]
    skipped["evidence_manifest_digest"] = None
    assert CampaignResult.model_validate(skipped).state == "skipped"

    missing_reason = deepcopy(skipped)
    missing_reason["cases"][0]["reason"] = None  # type: ignore[index]
    with pytest.raises(ValidationError, match="skipped cases require a reason"):
        CampaignResult.model_validate(missing_reason)

    mixed = deepcopy(skipped)
    mixed["cases"][0]["state"] = "inconclusive"  # type: ignore[index]
    with pytest.raises(ValidationError, match="requires skipped cases"):
        CampaignResult.model_validate(mixed)


def test_evidence_manifest_rejects_unsafe_paths_and_stays_immutable() -> None:
    manifest_data: dict[str, object] = {
        "schema_version": "1.0.0",
        "run_id": run_id_for("2026-07-12", SHA_A, SHA256_A),
        "campaign_id": "target-integrity/target-binding",
        "target_sha": SHA_A,
        "protocol_digest": SHA256_A,
        "configuration_digest": SHA256_A,
        "environment_digest": SHA256_A,
        "producer": {"nef_sha": SHA_A, "tool_versions": {"python": "3.12.13"}},
        "objects": [
            {
                "path": "raw/result.json",
                "media_type": "application/json",
                "size_bytes": 10,
                "sha256": SHA256_A,
            }
        ],
        "sealed_at": "2026-07-12T13:05:02Z",
    }
    manifest = EvidenceManifest.model_validate(manifest_data)
    assert manifest.objects[0].path == "raw/result.json"

    unsafe = deepcopy(manifest_data)
    unsafe["objects"][0]["path"] = "../result.json"  # type: ignore[index]
    with pytest.raises(ValidationError, match="relative and traversal-free"):
        EvidenceManifest.model_validate(unsafe)


def test_finding_fingerprint_excludes_run_identity_and_disposition_is_human_data() -> None:
    fingerprint = finding_fingerprint(
        source="deterministic",
        title="Moved target tag",
        claim="A previously observed gate binding changed.",
        severity="high",
    )
    finding_data = {
        "schema_version": "1.0.0",
        "fingerprint": fingerprint,
        "authority": "candidate",
        "source": "deterministic",
        "title": "Moved target tag",
        "claim": "A previously observed gate binding changed.",
        "severity": "high",
        "evidence_digests": [SHA256_A],
        "first_seen_run_id": "run-one",
        "last_seen_run_id": "run-two",
    }
    finding = Finding.model_validate(finding_data)
    assert finding.fingerprint == fingerprint

    recurrence = {**finding_data, "first_seen_run_id": "another", "last_seen_run_id": "latest"}
    assert Finding.model_validate(recurrence).fingerprint == fingerprint

    wrong = {**finding_data, "fingerprint": "b" * 64}
    with pytest.raises(ValidationError, match="finding fingerprint mismatch"):
        Finding.model_validate(wrong)

    disposition = Disposition.model_validate(
        {
            "schema_version": "1.0.0",
            "finding_fingerprint": fingerprint,
            "decision": "needs-more-evidence",
            "actor": "Matthias",
            "decided_at": "2026-07-12T13:06:00Z",
            "rationale": "Awaiting independent reproduction.",
            "evidence_digests": [SHA256_A],
            "run_ids": ["run-one"],
        }
    )
    assert disposition.actor == "Matthias"
