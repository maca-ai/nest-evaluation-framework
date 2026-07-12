"""Read-only command-line access to NEF contracts and aggregation."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from nef.contracts import (
    CONTRACT_MODELS,
    CampaignResult,
    canonical_json_text,
    generated_schema,
    validate_contract,
)
from nef.engine import aggregate_campaigns


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nef")
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate one contract JSON object")
    validate.add_argument("contract", choices=sorted(CONTRACT_MODELS))
    validate.add_argument("path", type=Path)
    validate.add_argument(
        "--peel-binding",
        action="append",
        default=[],
        metavar="TAG_REF_SHA=PEELED_SHA",
        help="supply previously resolved annotated-tag peel evidence",
    )

    schema = commands.add_parser("schema", help="emit a generated validation schema")
    schema.add_argument("contract", choices=sorted(CONTRACT_MODELS))

    aggregate = commands.add_parser("aggregate", help="aggregate campaign result JSON")
    aggregate.add_argument("path", type=Path)
    aggregate.add_argument("--required", action="append", required=True, metavar="CAMPAIGN_ID")
    return parser


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _object(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("contract input must be a JSON object")
    return value


def _peel_bindings(values: Sequence[str]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for value in values:
        tag_ref, separator, peeled = value.partition("=")
        if not separator or not tag_ref or not peeled:
            raise ValueError("peel binding must use TAG_REF_SHA=PEELED_SHA")
        if tag_ref in bindings and bindings[tag_ref] != peeled:
            raise ValueError("one tag-ref SHA cannot have conflicting peel bindings")
        bindings[tag_ref] = peeled
    return bindings


def _results(value: Any) -> tuple[CampaignResult, ...]:
    if not isinstance(value, list):
        raise ValueError("aggregate input must be a JSON array")
    return tuple(CampaignResult.model_validate(_object(item)) for item in value)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the read-only CLI and return a process exit status."""
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            bindings = _peel_bindings(args.peel_binding)
            contract = validate_contract(
                args.contract,
                _object(_read_json(args.path)),
                peel_bindings=bindings or None,
            )
            output: object = contract
        elif args.command == "schema":
            output = generated_schema(args.contract)
        else:
            output = aggregate_campaigns(_results(_read_json(args.path)), args.required)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    sys.stdout.write(canonical_json_text(output) + "\n")
    return 0
