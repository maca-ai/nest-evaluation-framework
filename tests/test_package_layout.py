from __future__ import annotations

import importlib
import re
from pathlib import Path

import yaml  # type: ignore[import-untyped]

import nef


def test_expected_public_package_boundaries_import() -> None:
    assert nef.__version__ == "0.1.0"
    for module in ("contracts", "engine", "target", "weapons", "evidence", "report"):
        importlib.import_module(f"nef.{module}")


def test_workflow_actions_are_full_commit_shas() -> None:
    uses_pattern = re.compile(r"^\s*-?\s*uses:\s*[^@\s]+@([0-9a-f]{40})(?:\s+#.*)?$")
    workflows = sorted(Path(".github/workflows").glob("*.yml"))
    assert workflows
    for workflow in workflows:
        document = yaml.safe_load(workflow.read_text(encoding="utf-8"))
        assert isinstance(document, dict)
        for line in workflow.read_text(encoding="utf-8").splitlines():
            if "uses:" in line:
                assert uses_pattern.match(line), f"unpinned action in {workflow}: {line}"


def test_disposable_targets_are_ignored() -> None:
    ignored = Path(".gitignore").read_text(encoding="utf-8").splitlines()
    assert "/.targets/" in ignored
    assert ".env" in ignored
    assert ".DS_Store" in ignored
