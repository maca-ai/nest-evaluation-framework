"""Offline CLI verification tests."""

from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture

from nef.cli import main
from nef.contracts import EvidenceManifest, canonical_json_text
from nef.evidence import EvidenceStore
from tests.contract_fixtures import evidence_manifest_data


def sealed_store(root: Path) -> tuple[EvidenceStore, str]:
    store = EvidenceStore(root)
    value = {"state": "pass"}
    evidence = store.put_json("raw/result.json", value)
    data = evidence_manifest_data()
    data["objects"] = [evidence.model_dump(mode="json")]
    manifest = EvidenceManifest.model_validate(data)
    verified = store.seal(manifest, maximum_retention_days=400)
    return store, verified.manifest_digest


def test_verify_command_emits_canonical_summary(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    _, digest = sealed_store(tmp_path)

    assert main(["verify", str(tmp_path), digest]) == 0
    captured = capsys.readouterr()
    assert (
        captured.out
        == canonical_json_text(
            {
                "manifest_digest": digest,
                "object_count": 1,
                "retention": {
                    "assurance": "policy-intent-not-permanence",
                    "observed_maximum_days": 400,
                    "requested_days": 400,
                },
                "verified": True,
            }
        )
        + "\n"
    )
    assert captured.err == ""


def test_verify_command_fails_closed_for_malformed_manifest(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    _, digest = sealed_store(tmp_path)
    path = tmp_path / "evidence/v1/manifests/sha256" / digest[:2] / f"{digest}.json"
    path.write_text(json.dumps({"bad": True}), encoding="utf-8")

    assert main(["verify", str(tmp_path), digest]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error:" in captured.err
