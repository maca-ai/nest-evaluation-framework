"""Deterministic campaign used by shared conformance tests and adapters."""

from __future__ import annotations

from nef.contracts import (
    CampaignRequest,
    CampaignResult,
    EvaluationState,
    canonical_sha256,
)


class DeterministicFakeCampaign:
    """Emit one configured state without target access or ambient input."""

    def __init__(self, state: EvaluationState) -> None:
        self._state = state

    def execute(self, request: CampaignRequest) -> CampaignResult:
        reason = None if self._state == "pass" else f"configured {self._state}"
        evidence_digest = canonical_sha256(
            {
                "campaign_id": request.campaign_id,
                "run_id": request.run_id,
                "state": self._state,
            }
        )
        result = CampaignResult.model_validate(
            {
                "schema_version": "1.0.0",
                "run_id": request.run_id,
                "campaign_id": request.campaign_id,
                "state": self._state,
                "required": True,
                "started_at": "2000-01-01T00:00:00Z",
                "finished_at": "2000-01-01T00:00:00Z",
                "cases": [
                    {
                        "case_id": "fake/configured-state",
                        "state": self._state,
                        "reason": reason,
                        "evidence_digests": [evidence_digest] if self._state == "pass" else [],
                    }
                ],
                "measurements": {"deterministic": True},
                "candidate_finding_fingerprints": [],
                "replay_metadata": {
                    "replayable": True,
                    "data": {"configured_state": self._state},
                },
                "budget_use": {
                    "elapsed_seconds": "0",
                    "cost_eur": "0",
                    "peak_memory_mib": 0,
                    "output_bytes": 0,
                },
                "evidence_manifest_digest": evidence_digest if self._state == "pass" else None,
            }
        )
        self.assert_request_identity(request, result)
        return result

    @staticmethod
    def assert_request_identity(request: CampaignRequest, result: CampaignResult) -> None:
        """Reject adapters that return a result for a different request identity."""
        if result.run_id != request.run_id or result.campaign_id != request.campaign_id:
            raise ValueError("campaign result identity does not match request identity")
