"""The single public campaign execution seam."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from nef.contracts import CampaignRequest, CampaignResult


@runtime_checkable
class Campaign(Protocol):
    """Execute one campaign against a validated immutable request."""

    def execute(self, request: CampaignRequest) -> CampaignResult:
        """Return the validated result for one campaign execution."""
        ...
