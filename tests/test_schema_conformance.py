from __future__ import annotations

import json
from copy import deepcopy
from functools import reduce
from pathlib import Path
from typing import Any, cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from jsonschema.exceptions import (  # type: ignore[import-untyped]
    ValidationError as JsonSchemaValidationError,
)
from pydantic import ValidationError as PydanticValidationError
from referencing import Registry, Resource

from nef.contracts import CONTRACT_MODELS, canonical_json_bytes, generated_schema, validate_contract
from tests.contract_fixtures import VALID_CONTRACT_DATA

CONTRACTS = Path("specs/001-framework-contracts/contracts")


def load_normative(name: str) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((CONTRACTS / f"{name}.schema.json").read_text(encoding="utf-8")),
    )


def normative_validator(name: str) -> Draft202012Validator:
    schemas = [json.loads(path.read_text(encoding="utf-8")) for path in CONTRACTS.glob("*.json")]
    registry = reduce(
        lambda current, schema: current.with_resource(
            schema["$id"], Resource.from_contents(schema)
        ),
        schemas,
        Registry(),
    )
    return Draft202012Validator(load_normative(name), registry=registry)


@pytest.mark.parametrize("contract_name", sorted(VALID_CONTRACT_DATA))
def test_generated_schema_matches_normative_required_and_closed_behavior(
    contract_name: str,
) -> None:
    data = VALID_CONTRACT_DATA[contract_name]()
    normative = normative_validator(contract_name)
    generated = Draft202012Validator(generated_schema(contract_name))

    normative.validate(data)
    generated.validate(data)
    model = validate_contract(contract_name, data)
    normative.validate(model.model_dump(mode="json"))
    generated.validate(model.model_dump(mode="json"))

    missing_required = deepcopy(data)
    first_required = load_normative(contract_name)["required"][0]
    missing_required.pop(first_required)
    with pytest.raises(JsonSchemaValidationError):
        normative.validate(missing_required)
    with pytest.raises(JsonSchemaValidationError):
        generated.validate(missing_required)
    with pytest.raises(PydanticValidationError):
        validate_contract(contract_name, missing_required)

    unknown = {**data, "unexpected": True}
    with pytest.raises(JsonSchemaValidationError):
        normative.validate(unknown)
    with pytest.raises(JsonSchemaValidationError):
        generated.validate(unknown)
    with pytest.raises(PydanticValidationError):
        validate_contract(contract_name, unknown)


def test_all_eight_generated_schemas_are_deterministic_draft_2020_12() -> None:
    assert set(CONTRACT_MODELS) == set(VALID_CONTRACT_DATA)
    for contract_name in sorted(CONTRACT_MODELS):
        schema = generated_schema(contract_name)
        Draft202012Validator.check_schema(schema)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert canonical_json_bytes(schema) == canonical_json_bytes(generated_schema(contract_name))


def assert_normative_generated_and_code_reject(name: str, data: dict[str, Any]) -> None:
    with pytest.raises(JsonSchemaValidationError):
        normative_validator(name).validate(data)
    with pytest.raises(JsonSchemaValidationError):
        Draft202012Validator(generated_schema(name)).validate(data)
    with pytest.raises(PydanticValidationError):
        validate_contract(name, data)


def test_generated_schemas_preserve_normative_unique_array_constraints() -> None:
    snapshot = VALID_CONTRACT_DATA["target-snapshot-manifest"]()
    snapshot["consulted_paths"] = ["AGENTS.md", "AGENTS.md"]
    assert_normative_generated_and_code_reject("target-snapshot-manifest", snapshot)

    capabilities = VALID_CONTRACT_DATA["target-capability-manifest"]()
    capabilities["required_campaigns"] = [
        "target-integrity/target-binding",
        "target-integrity/target-binding",
    ]
    assert_normative_generated_and_code_reject("target-capability-manifest", capabilities)

    result = VALID_CONTRACT_DATA["campaign-result"]()
    result["candidate_finding_fingerprints"] = ["a" * 64, "a" * 64]
    assert_normative_generated_and_code_reject("campaign-result", result)

    finding = VALID_CONTRACT_DATA["finding"]()
    finding["evidence_digests"] = ["a" * 64, "a" * 64]
    assert_normative_generated_and_code_reject("finding", finding)

    disposition = VALID_CONTRACT_DATA["disposition"]()
    disposition["run_ids"] = ["run-one", "run-one"]
    assert_normative_generated_and_code_reject("disposition", disposition)


def test_generated_snapshot_schema_preserves_nonempty_source_digest_keys() -> None:
    snapshot = VALID_CONTRACT_DATA["target-snapshot-manifest"]()
    snapshot["relevant_source_digests"] = {"": "a" * 64}
    assert_normative_generated_and_code_reject("target-snapshot-manifest", snapshot)


def test_generated_schemas_preserve_normative_conditional_constraints() -> None:
    capabilities = VALID_CONTRACT_DATA["target-capability-manifest"]()
    capabilities["capabilities"][0]["state"] = "unavailable"
    capabilities["capabilities"][0].pop("reason")
    assert_normative_generated_and_code_reject("target-capability-manifest", capabilities)

    snapshot = VALID_CONTRACT_DATA["target-snapshot-manifest"]()
    snapshot.update(
        {
            "target_mode": "gate-evidence",
            "selector": {"kind": "gate-tag", "gate_tag": "m0", "tag_ref_sha": "a" * 40},
            "evidence_class": "gate-evidence",
            "baseline_reproducibility": "reproducible-baseline",
            "tag_binding": {
                "state": "unchanged",
                "previous_snapshot_manifest_digest": None,
                "previous_tag_ref_sha": None,
                "previous_resolved_sha": None,
            },
        }
    )
    assert_normative_generated_and_code_reject("target-snapshot-manifest", snapshot)
