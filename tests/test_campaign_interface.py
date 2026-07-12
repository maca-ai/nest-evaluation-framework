from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from nef.contracts import CampaignRequest, CampaignResult, EvaluationState
from nef.engine.campaign import Campaign
from nef.engine.fake import DeterministicFakeCampaign
from tests.campaign_conformance import assert_campaign_conformance
from tests.contract_fixtures import campaign_request_data, campaign_result_data


def request() -> CampaignRequest:
    return CampaignRequest.model_validate(campaign_request_data())


def test_deterministic_fake_campaign_satisfies_shared_conformance_suite() -> None:
    assert_campaign_conformance(DeterministicFakeCampaign, request())
    assert isinstance(DeterministicFakeCampaign("pass"), Campaign)


class IdentityDriftingCampaign:
    def execute(self, request: CampaignRequest) -> CampaignResult:
        data = campaign_result_data()
        data["run_id"] = "wrong-run"
        return CampaignResult.model_validate(data)


def test_shared_conformance_suite_detects_identity_drift() -> None:
    def drifting_factory(state: EvaluationState) -> Campaign:
        del state
        return IdentityDriftingCampaign()

    with pytest.raises(AssertionError):
        assert_campaign_conformance(drifting_factory, request())


@pytest.mark.parametrize(
    ("field", "value"),
    [("run_id", "wrong-run"), ("campaign_id", "wrong/campaign")],
)
def test_result_contract_rejects_adapter_identity_drift(field: str, value: str) -> None:
    data = deepcopy(campaign_result_data())
    data[field] = value
    result = CampaignResult.model_validate(data)
    with pytest.raises(ValueError, match="identity"):
        DeterministicFakeCampaign.assert_request_identity(request(), result)


def test_result_contract_rejects_false_pass_without_evidence() -> None:
    data = deepcopy(campaign_result_data())
    data["evidence_manifest_digest"] = None
    with pytest.raises(ValidationError, match="pass requires an evidence manifest"):
        CampaignResult.model_validate(data)


def test_fake_preserves_each_nonpass_state_without_collapsing() -> None:
    states: tuple[EvaluationState, ...] = (
        "fail",
        "error",
        "inconclusive",
        "invalid",
        "skipped",
    )
    assert [DeterministicFakeCampaign(state).execute(request()).state for state in states] == [
        "fail",
        "error",
        "inconclusive",
        "invalid",
        "skipped",
    ]
