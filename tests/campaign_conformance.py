"""Reusable conformance assertions for Campaign implementations."""

from __future__ import annotations

from collections.abc import Callable

from nef.contracts import CampaignRequest, CampaignResult, EvaluationState, canonical_json_bytes
from nef.engine.campaign import Campaign


def assert_campaign_conformance(
    campaign_factory: Callable[[EvaluationState], Campaign],
    request: CampaignRequest,
) -> None:
    """Assert deterministic identity preservation and exact state vocabulary."""
    states: tuple[EvaluationState, ...] = (
        "pass",
        "fail",
        "error",
        "inconclusive",
        "invalid",
        "skipped",
    )
    for state in states:
        campaign = campaign_factory(state)
        first = campaign.execute(request)
        second = campaign.execute(request)
        assert isinstance(first, CampaignResult)
        assert first.run_id == request.run_id
        assert first.campaign_id == request.campaign_id
        assert first.state == state
        assert canonical_json_bytes(first) == canonical_json_bytes(second)
