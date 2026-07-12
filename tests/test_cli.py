from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from pytest import CaptureFixture

from nef.cli import main
from nef.contracts import canonical_json_text
from tests.contract_fixtures import (
    SHA_A,
    SHA_B,
    campaign_result_data,
    target_descriptor_data,
)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def test_validate_emits_canonical_contract_json(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "descriptor.json"
    data = target_descriptor_data()
    write_json(path, data)

    assert main(["validate", "target-descriptor", str(path)]) == 0
    captured = capsys.readouterr()
    assert captured.out == canonical_json_text(data) + "\n"
    assert captured.err == ""


def test_validate_accepts_explicit_annotated_peel_evidence(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "descriptor.json"
    data = target_descriptor_data()
    data.update(
        {
            "target_mode": "gate-evidence",
            "selector": {"kind": "gate-tag", "gate_tag": "m0", "tag_ref_sha": SHA_B},
        }
    )
    write_json(path, data)

    assert (
        main(["validate", "target-descriptor", str(path), "--peel-binding", f"{SHA_B}={SHA_A}"])
        == 0
    )
    assert capsys.readouterr().err == ""


def test_validate_refuses_missing_peel_evidence(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "descriptor.json"
    data = target_descriptor_data()
    data.update(
        {
            "target_mode": "gate-evidence",
            "selector": {"kind": "gate-tag", "gate_tag": "m0", "tag_ref_sha": SHA_B},
        }
    )
    write_json(path, data)

    assert main(["validate", "target-descriptor", str(path)]) == 1
    assert "peel evidence" in capsys.readouterr().err


def test_schema_emits_generated_draft_2020_12_json(capsys: CaptureFixture[str]) -> None:
    assert main(["schema", "campaign-result"]) == 0
    captured = capsys.readouterr()
    schema = json.loads(captured.out)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_aggregate_preserves_precedence(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    passing = campaign_result_data()
    failing = deepcopy(campaign_result_data())
    failing["campaign_id"] = "target-integrity/other"
    failing["state"] = "fail"
    failing["cases"][0]["state"] = "fail"
    failing["cases"][0]["reason"] = "sabotage"
    failing["evidence_manifest_digest"] = None
    path = tmp_path / "results.json"
    write_json(path, [passing, failing])

    assert (
        main(
            [
                "aggregate",
                str(path),
                "--required",
                "target-integrity/target-binding",
                "--required",
                "target-integrity/other",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out == '"fail"\n'


def test_validate_rejects_non_object_input(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "bad.json"
    write_json(path, [])
    assert main(["validate", "finding", str(path)]) == 1
    assert "JSON object" in capsys.readouterr().err
