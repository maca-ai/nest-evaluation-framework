"""Constitution-ordered campaign aggregation."""

from __future__ import annotations

from collections.abc import Iterable

from nef.contracts import CampaignResult, EvaluationState


def aggregate_campaigns(
    results: Iterable[CampaignResult], required_campaign_ids: Iterable[str]
) -> EvaluationState:
    """Aggregate without collapsing product, harness, or evidence states."""
    required_sequence = tuple(required_campaign_ids)
    required = frozenset(required_sequence)
    if not required or len(required) != len(required_sequence):
        return "invalid"

    collected = tuple(results)
    by_id = {result.campaign_id: result for result in collected}
    if len(by_id) != len(collected):
        return "error"
    if any(result.required != (result.campaign_id in required) for result in collected):
        return "error"

    if any(result.state == "error" for result in collected):
        return "error"
    if any(result.state == "fail" for result in collected):
        return "fail"
    if not required.issubset(by_id):
        return "inconclusive"
    incomplete_states = {"inconclusive", "invalid", "skipped"}
    if any(by_id[campaign_id].state in incomplete_states for campaign_id in required):
        return "inconclusive"
    if all(by_id[campaign_id].state == "pass" for campaign_id in required):
        return "pass"
    return "inconclusive"
