"""Conformance and sabotage tests for the local evidence store."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from nef.contracts import (
    EvidenceManifest,
    EvidenceProducer,
    canonical_json_bytes,
    canonical_sha256,
)
from nef.evidence import (
    EvidenceConflictError,
    EvidenceIntegrityError,
    EvidenceStore,
    RetentionSetupError,
    SensitiveEvidenceError,
)
from tests.contract_fixtures import evidence_manifest_data


def manifest_for(result: object) -> tuple[EvidenceManifest, object]:
    data = evidence_manifest_data()
    encoded = canonical_json_bytes(result)
    data["objects"] = [
        {
            "path": "raw/result.json",
            "media_type": "application/json",
            "size_bytes": len(encoded),
            "sha256": canonical_sha256(result),
        }
    ]
    return EvidenceManifest.model_validate(data), result


def blob_path(root: Path, digest: str) -> Path:
    return root / "evidence/v1/blobs/sha256" / digest[:2] / f"{digest}.json"


def manifest_path(root: Path, digest: str) -> Path:
    return root / "evidence/v1/manifests/sha256" / digest[:2] / f"{digest}.json"


def retention_path(root: Path, digest: str) -> Path:
    return root / "evidence/v1/bundles" / digest / "retention.json"


def test_put_json_uses_the_shared_canonical_content_address(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    value = {"z": [True, 7], "a": "utf-8: ö"}

    evidence = store.put_json("raw/result.json", value)

    assert evidence.sha256 == canonical_sha256(value)
    assert evidence.size_bytes == len(canonical_json_bytes(value))
    assert evidence.media_type == "application/json"
    assert blob_path(tmp_path, evidence.sha256).read_bytes() == canonical_json_bytes(value)


def test_identical_duplicate_write_is_idempotent(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    first = store.put_json("raw/result.json", {"state": "pass"})
    second = store.put_json("raw/result.json", {"state": "pass"})

    assert first == second


def test_conflicting_existing_digest_path_is_never_overwritten(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    value = {"state": "pass"}
    digest = canonical_sha256(value)
    path = blob_path(tmp_path, digest)
    path.parent.mkdir(parents=True)
    path.write_bytes(b"sabotage")

    with pytest.raises(EvidenceConflictError, match="different bytes"):
        store.put_json("raw/result.json", value)

    assert path.read_bytes() == b"sabotage"


def test_seal_writes_manifest_last_and_verify_returns_validated_evidence(
    tmp_path: Path,
) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass", "measurements": {"checks": 1}})
    store.put_json("raw/result.json", result)

    verified = store.seal(manifest, maximum_retention_days=400)

    assert verified.manifest == manifest
    assert verified.manifest_digest == canonical_sha256(manifest)
    assert verified.object_count == 1
    assert verified.retention.requested_days == 400
    assert verified.retention.observed_maximum_days == 400
    assert manifest_path(tmp_path, verified.manifest_digest).is_file()
    assert store.verify(verified.manifest_digest) == verified


@pytest.mark.parametrize("maximum", [None, 399])
def test_seal_refuses_unverified_or_short_retention(tmp_path: Path, maximum: int | None) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    store.put_json("raw/result.json", result)

    with pytest.raises(RetentionSetupError, match="400"):
        store.seal(manifest, maximum_retention_days=maximum)

    assert not manifest_path(tmp_path, canonical_sha256(manifest)).exists()


def test_verify_rejects_tampered_blob(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    evidence = store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    blob_path(tmp_path, evidence.sha256).write_bytes(canonical_json_bytes({"state": "fail"}))

    with pytest.raises(EvidenceIntegrityError, match="digest"):
        store.verify(sealed.manifest_digest)


def test_verify_rejects_truncated_blob(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    evidence = store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    blob_path(tmp_path, evidence.sha256).write_bytes(b'{"state"')

    with pytest.raises(EvidenceIntegrityError, match="JSON"):
        store.verify(sealed.manifest_digest)


def test_verify_rejects_missing_blob(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    evidence = store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    blob_path(tmp_path, evidence.sha256).unlink()

    with pytest.raises(EvidenceIntegrityError, match="missing"):
        store.verify(sealed.manifest_digest)


def test_seal_does_not_create_manifest_when_a_blob_is_missing(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, _ = manifest_for({"state": "pass"})
    digest = canonical_sha256(manifest)

    with pytest.raises(EvidenceIntegrityError, match="missing"):
        store.seal(manifest, maximum_retention_days=400)

    assert not manifest_path(tmp_path, digest).exists()
    assert not retention_path(tmp_path, digest).exists()


def test_verify_rejects_malformed_manifest(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    manifest_path(tmp_path, sealed.manifest_digest).write_bytes(b"{}")

    with pytest.raises(EvidenceIntegrityError, match="manifest"):
        store.verify(sealed.manifest_digest)


def test_verify_rejects_noncanonical_manifest_bytes(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    path = manifest_path(tmp_path, sealed.manifest_digest)
    path.write_text(json.dumps(manifest.model_dump(mode="json"), indent=2), encoding="utf-8")

    with pytest.raises(EvidenceIntegrityError, match="canonical"):
        store.verify(sealed.manifest_digest)


def test_verify_rejects_missing_retention_metadata(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    retention_path(tmp_path, sealed.manifest_digest).unlink()

    with pytest.raises(EvidenceIntegrityError, match="missing"):
        store.verify(sealed.manifest_digest)


def test_verify_rejects_retention_downgrade(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    path = retention_path(tmp_path, sealed.manifest_digest)
    record = json.loads(path.read_text(encoding="utf-8"))
    record["observed_maximum_days"] = 30
    path.write_bytes(canonical_json_bytes(record))

    with pytest.raises(EvidenceIntegrityError, match="400-day"):
        store.verify(sealed.manifest_digest)


def test_verify_refuses_a_symlinked_blob(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    evidence = store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    path = blob_path(tmp_path, evidence.sha256)
    replacement = tmp_path / "replacement.json"
    replacement.write_bytes(canonical_json_bytes(result))
    path.unlink()
    path.symlink_to(replacement)

    with pytest.raises(EvidenceIntegrityError, match="regular file"):
        store.verify(sealed.manifest_digest)


@pytest.mark.parametrize(
    ("logical_path", "value"),
    [
        ("raw/.env", {"safe": True}),
        ("raw/.env.production", {"safe": True}),
        ("raw/credentials.json", {"safe": True}),
        ("raw/result.json", {"private_key": "synthetic-but-forbidden"}),
        ("raw/result.json", {"text": "-----" + "BEGIN PRIVATE KEY-----"}),
        ("raw/result.json", {"token": "ghp_" + "a" * 32}),
    ],
)
def test_put_json_rejects_detectable_sensitive_evidence(
    tmp_path: Path, logical_path: str, value: object
) -> None:
    with pytest.raises(SensitiveEvidenceError):
        EvidenceStore(tmp_path).put_json(logical_path, value)


def test_put_json_scans_canonicalized_contract_values(tmp_path: Path) -> None:
    producer = EvidenceProducer(
        nef_sha="a" * 40,
        tool_versions={"token": "detect-me-after-model-serialization"},
    )

    with pytest.raises(SensitiveEvidenceError):
        EvidenceStore(tmp_path).put_json("raw/producer.json", producer)


def test_verify_rejects_detectable_secret_injected_after_sealing(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path)
    manifest, result = manifest_for({"state": "pass"})
    evidence = store.put_json("raw/result.json", result)
    sealed = store.seal(manifest, maximum_retention_days=400)
    injected = {"token": "ghp_" + "a" * 32}
    path = blob_path(tmp_path, evidence.sha256)
    path.write_bytes(canonical_json_bytes(injected))

    with pytest.raises(SensitiveEvidenceError):
        store.verify(sealed.manifest_digest)


def test_float_evidence_is_rejected_by_shared_canonicalizer(tmp_path: Path) -> None:
    with pytest.raises(TypeError, match="floats are forbidden"):
        EvidenceStore(tmp_path).put_json("raw/result.json", {"ratio": 0.5})
