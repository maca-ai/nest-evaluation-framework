from __future__ import annotations

from copy import deepcopy

import pytest

from nef.contracts import CampaignResult, EvaluationState
from nef.engine import aggregate_campaigns
from tests.contract_fixtures import campaign_result_data


def result(
    state: EvaluationState,
    campaign_id: str,
    *,
    required: bool = True,
) -> CampaignResult:
    data = deepcopy(campaign_result_data())
    data["campaign_id"] = campaign_id
    data["state"] = state
    data["required"] = required
    if state != "pass":
        data["cases"][0]["state"] = state
        data["cases"][0]["reason"] = f"configured {state}"
        data["evidence_manifest_digest"] = None
    return CampaignResult.model_validate(data)


def test_aggregation_follows_constitution_precedence_without_state_collapse() -> None:
    required = ("campaign/one", "campaign/two")
    passing = [result("pass", campaign_id) for campaign_id in required]
    assert aggregate_campaigns(passing, required) == "pass"

    incomplete = [result("inconclusive", "campaign/one"), result("skipped", "campaign/two")]
    assert aggregate_campaigns(incomplete, required) == "inconclusive"

    with_failure = [result("fail", "campaign/one"), result("invalid", "campaign/two")]
    assert aggregate_campaigns(with_failure, required) == "fail"

    with_error = [result("error", "campaign/one"), result("fail", "campaign/two")]
    assert aggregate_campaigns(with_error, required) == "error"


@pytest.mark.parametrize("state", ["inconclusive", "invalid", "skipped"])
def test_each_required_incomplete_state_remains_inconclusive(state: EvaluationState) -> None:
    assert aggregate_campaigns([result(state, "campaign/one")], ("campaign/one",)) == (
        "inconclusive"
    )


def test_aggregation_rejects_empty_missing_duplicate_or_requiredness_mismatch() -> None:
    assert aggregate_campaigns([], ()) == "invalid"
    assert aggregate_campaigns([], ("campaign/one",)) == "inconclusive"

    duplicate = [result("pass", "campaign/one"), result("pass", "campaign/one")]
    assert aggregate_campaigns(duplicate, ("campaign/one",)) == "error"

    mismatched = [result("pass", "campaign/one", required=False)]
    assert aggregate_campaigns(mismatched, ("campaign/one",)) == "error"


def test_optional_skip_does_not_falsify_complete_required_passes() -> None:
    results = [
        result("pass", "campaign/required"),
        result("skipped", "campaign/optional", required=False),
    ]
    assert aggregate_campaigns(results, ("campaign/required",)) == "pass"
