"""Shared valid contract data for schema, CLI, and campaign conformance tests."""

from __future__ import annotations

from typing import Any

from nef.contracts import (
    FindingSeverity,
    FindingSource,
    canonical_sha256,
    finding_fingerprint,
    run_id_for,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA256_A = "a" * 64


def target_descriptor_data() -> dict[str, Any]:
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
        "observed_at": "2026-07-12T13:05:01Z",
        "source_kind": "remote",
    }


def target_snapshot_data() -> dict[str, Any]:
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


def target_capability_data() -> dict[str, Any]:
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


def campaign_request_data() -> dict[str, Any]:
    snapshot = target_snapshot_data()
    capabilities = target_capability_data()
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


def campaign_result_data() -> dict[str, Any]:
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


def evidence_manifest_data() -> dict[str, Any]:
    return {
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


def finding_data() -> dict[str, Any]:
    source: FindingSource = "deterministic"
    title = "Moved target tag"
    claim = "A previously observed gate binding changed."
    severity: FindingSeverity = "high"
    return {
        "schema_version": "1.0.0",
        "fingerprint": finding_fingerprint(
            source=source, title=title, claim=claim, severity=severity
        ),
        "authority": "candidate",
        "source": source,
        "title": title,
        "claim": claim,
        "severity": severity,
        "evidence_digests": [SHA256_A],
        "first_seen_run_id": "run-one",
        "last_seen_run_id": "run-one",
    }


def disposition_data() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "finding_fingerprint": finding_data()["fingerprint"],
        "decision": "needs-more-evidence",
        "actor": "Matthias",
        "decided_at": "2026-07-12T13:06:00Z",
        "rationale": "Awaiting independent reproduction.",
        "evidence_digests": [SHA256_A],
        "run_ids": ["run-one"],
    }


VALID_CONTRACT_DATA = {
    "target-descriptor": target_descriptor_data,
    "target-snapshot-manifest": target_snapshot_data,
    "target-capability-manifest": target_capability_data,
    "campaign-request": campaign_request_data,
    "campaign-result": campaign_result_data,
    "evidence-manifest": evidence_manifest_data,
    "finding": finding_data,
    "disposition": disposition_data,
}
