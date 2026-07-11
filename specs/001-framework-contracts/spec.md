# Feature specification: Framework contracts, evidence, and orchestration

**Spec:** NEF-001
**Status:** Approved for NEF-T001 implementation
**Schema version:** 1.0.0
**Depends on:** NEF constitution

## Goal

Provide one provider-neutral contract and evidence layer through which every NEF campaign runs, so product failure, harness failure, missing evidence, invalid cases, and capability skips remain reproducible and distinct.

## User story 1 - One campaign seam

As a campaign author, I implement one deep interface and receive explicit target, capability, budget, configuration, workspace, and replay inputs.

### Acceptance scenarios

1. Given any integrity, mutation, fuzz, performance, or model-audit adapter, when it executes, then it is invoked through `Campaign.execute(CampaignRequest) -> CampaignResult`.
2. Given unknown request or result fields, when the contract validates, then validation refuses them.
3. Given a result labeled `pass` without a sealed evidence-manifest digest, when validated or aggregated, then it is refused and cannot make the run pass.
4. Given a campaign timeout or cancellation, when the adapter terminates, then it returns or is normalized to an explicit non-pass state with retained partial evidence.

## User story 2 - Evidence precedes grading

As an investigator, I can verify the raw evidence independently and rebuild the report without executing target code or contacting a provider.

### Acceptance scenarios

1. Given raw campaign output, when a grade is produced, then a content-addressed evidence manifest was sealed first.
2. Given a missing, truncated, or digest-mismatched blob, when the manifest is verified, then verification fails and no report treats the campaign as pass.
3. Given a duplicate content-addressed write with different bytes, when publication occurs, then the conflict is an error and the existing object is not overwritten.
4. Given only validated manifests, when the report builder runs twice, then its canonical report bytes are identical.

## User story 3 - Honest aggregation

As Matthias, I can tell whether a run found a NEST defect, suffered a harness error, lacked evidence, received invalid input, or deliberately skipped an unavailable capability.

### Acceptance scenarios

1. Given a required campaign `error` and another `fail`, when aggregated, then the run is `error`.
2. Given no required error and at least one product `fail`, when aggregated, then the run is `fail`.
3. Given only required passes plus a required `inconclusive`, `invalid`, or `skipped`, when aggregated, then the run is `inconclusive`.
4. Given complete required passes and only reasoned skips for non-required capabilities, when aggregated, then the run is `pass` while those skips remain visible.
5. Given missing evidence, when aggregation runs, then it cannot be converted to pass by defaulting or omission.

## User story 4 - Daily canonical attempt

As an operator, I receive one canonical result per scheduled date, target SHA, and protocol digest, while reruns remain separate attempts.

### Acceptance scenarios

1. Given the same scheduled date, target SHA, and protocol digest, when rerun, then attempt numbers increase without changing the base run identity.
2. Given concurrent dispatches, when canonical publication occurs, then one concurrency group prevents cancellation or replacement of an active canonical attempt.
3. Given no terminal manifest after 26 hours, when the best-effort watchdog observes the absence, then it publishes a harness incident and does not claim independent monitoring.
4. Given a scheduled event is delayed or dropped, when manual dispatch is used, then it preserves the same identity and explicit attempt semantics.

## User story 5 - Advisory findings lifecycle

As a triager, I receive stable candidate findings linked to evidence and record dated dispositions without automatic promotion or remediation.

### Acceptance scenarios

1. Given the same underlying claim recurs in two runs, when published, then the stable fingerprint identifies one finding and adds recurrence evidence.
2. Given a model candidate, when created, then its source is `model-supported` or `model-suspected` and its authority remains `candidate`.
3. Given no human decision, when a report renders, then it does not call the finding confirmed.
4. Given a disposition, when recorded, then actor, time, rationale, evidence, and run references are present.
5. Given a fixed or rejected disposition, when a later recurrence occurs, then NEF records recurrence rather than silently closing or reopening state.

## Functional requirements

- **NEF-001-FR-001:** Contracts MUST conform to the normative JSON Schemas under `contracts/` and use semantic version 1.0.0 initially.
- **NEF-001-FR-002:** The only public campaign execution seam MUST be `Campaign.execute(CampaignRequest) -> CampaignResult`.
- **NEF-001-FR-003:** Contracts MUST be immutable after validation and reject unknown fields.
- **NEF-001-FR-004:** Case and campaign states MUST be exactly `pass`, `fail`, `error`, `inconclusive`, `invalid`, and `skipped`.
- **NEF-001-FR-005:** Required-campaign aggregation MUST follow constitution III without state collapse.
- **NEF-001-FR-006:** A pass MUST reference a validated sealed evidence manifest and complete all required cases.
- **NEF-001-FR-007:** Raw evidence MUST be sealed before grading and reports MUST be deterministic projections from validated manifests only.
- **NEF-001-FR-008:** Canonical data MUST use UTF-8 sorted-key JSON, UTC timestamps, SHA-256, Decimal-as-string, and no floats in hashed or threshold-compared structures.
- **NEF-001-FR-009:** Run identity MUST be scheduled date plus target SHA plus protocol digest; attempts MUST be positive integers.
- **NEF-001-FR-010:** Campaign and case IDs MUST be stable across attempts; finding fingerprints MUST exclude run and attempt IDs.
- **NEF-001-FR-011:** Every campaign request MUST declare time, cost, memory, and output budgets.
- **NEF-001-FR-012:** Infrastructure/job timeout, cancellation, missing artifact, malformed output, evidence failure, and publication failure MUST be `error`; campaign-controlled insufficient sampling within a completed budget MUST be `inconclusive`.
- **NEF-001-FR-013:** The workflow MUST separate resolve, execute, model audit, aggregate, and publish permissions as defined by the trust model.
- **NEF-001-FR-014:** The daily workflow MUST support off-boundary schedule and manual dispatch with one non-canceling concurrency group.
- **NEF-001-FR-015:** The 26-hour missing-terminal-manifest watchdog MUST be described as best-effort and share no false independence claim.
- **NEF-001-FR-016:** Findings MUST be candidates until a human records a dated disposition.
- **NEF-001-FR-017:** Publication MUST be idempotent by stable finding fingerprint and MUST NOT close, remediate, promote, or change thresholds automatically.
- **NEF-001-FR-018:** Every campaign and the evidence store MUST ship a sabotage fixture demonstrating its claimed failure path.
- **NEF-001-FR-019:** Validated manifests and reports MUST be partitioned by target SHA, environment fingerprint, and protocol digest.
- **NEF-001-FR-020:** NEST spec 004 remains authoritative for NEST metrics; NEF may normalize names but MUST NOT promote thresholds.

## Data contracts

- `TargetDescriptor`
- `TargetSnapshotManifest`
- `TargetCapabilityManifest`
- `CampaignRequest`
- `CampaignResult`
- `EvidenceManifest`
- `Finding`
- `Disposition`

Field-level definitions and evolution rules are in `docs/public-interfaces.md` and the normative schemas.

## Edge cases

- Empty required campaign set is invalid, not a pass.
- A campaign process exits successfully but emits no result: `error`.
- A result references evidence that validates under a different target SHA or protocol digest: `invalid`.
- Two attempts claim the same canonical attempt number: publication error; neither silently overwrites the other.
- A non-required unavailable capability is reasoned `skipped`; a required campaign unexpectedly missing from the result set makes the run `inconclusive` or `error` according to whether evidence explains the absence.
- Model/provider outage cannot convert deterministic findings to error; it affects only the model campaign.

## Sabotage obligations

The conformance suite MUST include deliberate fixtures for every state, missing evidence, wrong digest, malformed manifest, conflicting content-addressed write, duplicate attempt, duplicate finding recurrence, and report nondeterminism. A suite that cannot fail each path fails NEF-001.

## Success criteria

- **NEF-001-SC-001:** All eight normative schemas parse and every implemented contract later conforms semantically.
- **NEF-001-SC-002:** Shared conformance proves all six states and missing-evidence behavior.
- **NEF-001-SC-003:** Rebuilding a report twice from the same validated manifests produces byte-identical canonical JSON.
- **NEF-001-SC-004:** Permission tests prove target execution has no provider secret/write permission and publisher executes no target code.
- **NEF-001-SC-005:** Every requirement maps to an acceptance scenario and later implementation task with no unresolved critical inconsistency.

## Non-goals

No Python implementation, workflow implementation, database, server, UI, provider configuration, or remote publication is part of NEF-T001.
