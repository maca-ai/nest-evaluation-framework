"""Contract model registry and generated validation schemas."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from nef.contracts.base import ContractModel
from nef.contracts.campaign import CampaignRequest, CampaignResult
from nef.contracts.evidence import EvidenceManifest
from nef.contracts.findings import Disposition, Finding
from nef.contracts.target import (
    TargetCapabilityManifest,
    TargetDescriptor,
    TargetSnapshotManifest,
)

CONTRACT_MODELS: dict[str, type[ContractModel]] = {
    "target-descriptor": TargetDescriptor,
    "target-snapshot-manifest": TargetSnapshotManifest,
    "target-capability-manifest": TargetCapabilityManifest,
    "campaign-request": CampaignRequest,
    "campaign-result": CampaignResult,
    "evidence-manifest": EvidenceManifest,
    "finding": Finding,
    "disposition": Disposition,
}

SCHEMA_IDS = {
    "target-descriptor": "https://maca-ai.github.io/nef/schemas/2.0.0/target-descriptor.schema.json",
    "target-snapshot-manifest": "https://maca-ai.github.io/nef/schemas/2.0.0/target-snapshot-manifest.schema.json",
    "target-capability-manifest": "https://maca-ai.github.io/nef/schemas/1.0.0/target-capability-manifest.schema.json",
    "campaign-request": "https://maca-ai.github.io/nef/schemas/2.0.0/campaign-request.schema.json",
    "campaign-result": "https://maca-ai.github.io/nef/schemas/1.0.0/campaign-result.schema.json",
    "evidence-manifest": "https://maca-ai.github.io/nef/schemas/1.0.0/evidence-manifest.schema.json",
    "finding": "https://maca-ai.github.io/nef/schemas/1.0.0/finding.schema.json",
    "disposition": "https://maca-ai.github.io/nef/schemas/1.0.0/disposition.schema.json",
}


def _contract_model(contract_name: str) -> type[ContractModel]:
    try:
        return CONTRACT_MODELS[contract_name]
    except KeyError as exc:
        choices = ", ".join(sorted(CONTRACT_MODELS))
        raise ValueError(f"unknown contract {contract_name!r}; expected one of: {choices}") from exc


def validate_contract(
    contract_name: str,
    data: Mapping[str, Any],
    *,
    peel_bindings: Mapping[str, str] | None = None,
) -> ContractModel:
    """Validate one contract, including semantic invariants absent from JSON Schema."""
    context = None if peel_bindings is None else {"peel_bindings": peel_bindings}
    return _contract_model(contract_name).model_validate(dict(data), context=context)


def generated_schema(contract_name: str) -> dict[str, Any]:
    """Generate one deterministic Draft 2020-12 validation schema from contract code."""
    model = _contract_model(contract_name)
    schema = deepcopy(model.model_json_schema(mode="validation", ref_template="#/$defs/{model}"))
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = SCHEMA_IDS[contract_name]
    return schema
