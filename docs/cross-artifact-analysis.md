# NEF-T001 cross-artifact analysis

**Run:** 2026-07-11
**Method:** Spec Kit analyze phase applied after the clarification record.
**Artifacts:** `AGENTS.md`, `PRD.md`, `PLANNING.md`, `TASKS.md`, NEF constitution 1.1.0, specs 001-006, eight normative JSON Schemas (three at 2.0.0 and five at 1.0.0), trust model, source matrix, retention contract, public interfaces, research register, and target profiles.

## Verdict

**Unresolved critical inconsistencies: 0.**

No requirement authorizes NEST modification, state collapse, missing-evidence success, model authority, automatic promotion, target-ref execution, customer/production data, production signing keys, or an invented T-016/Ed25519 interface.

## Product-to-implementation traceability

| PRD capability | Constitution | Specification / requirements | Contract or evidence | Implementation task | Sabotage proof |
|---|---|---|---|---|---|
| Daily orchestration, attempts, watchdog | III, IX, XI, XII | NEF-001 FR-009, FR-014, FR-015 | Campaign request/result, terminal manifests | NEF-T005 | delayed/missing run, duplicate attempt, cancellation |
| Shared engine and evidence | II-IV, VI | NEF-001 FR-001-FR-008, FR-018-FR-019 | All eight schemas, evidence manifest | NEF-T003, T004 | every state, missing/tampered evidence, nondeterministic report |
| Immutable target pinning and capabilities | I, V, VI | NEF-002 FR-001-FR-008, FR-014-FR-022 | Target descriptor/snapshot/capability schemas | NEF-T003, T005 | mutable selector, numeric ordering, annotated/lightweight peel, moved tag, wrong SHA, dirty target, false capability |
| Current hash-chain integrity | II, V | NEF-002 FR-009-FR-010 | Target profile and protocol digest | NEF-T005 | field tamper, genesis, gap, insertion/deletion/reorder/link/re-chain |
| T-016 conditional identity | V | NEF-002 FR-011, NEF-004 FR-009 | Source matrix unavailable entry | NEF-T005, T007 | reasoned skip now; namespace/transfer/conflict fixtures later |
| Ed25519 conditional signing | V, X | NEF-002 FR-012-FR-013, NEF-004 FR-010 | Source matrix unavailable entry | NEF-T002, T005, T007 | reasoned skip now; signature/key/re-chain fixtures later |
| Mutation | IV, VI | NEF-003 FR-001-FR-014 | Campaign request/result/evidence | NEF-T006 | controlled killed/survivor, denominator corruption, timeout |
| Property/stateful fuzz | IV, VI-VII | NEF-004 FR-001-FR-012 | Campaign result replay metadata/evidence | NEF-T007 | shrunk failure, stateful sequence, flaky replay, mismatch |
| Paired performance | VI-VII, XII | NEF-005 FR-001-FR-012 | Measurements/budget/evidence | NEF-T008 | slowdown, noise, missing pair, environment/protocol mismatch |
| Model audit | II, VIII-X, XII | NEF-006 FR-001-FR-012 | Finding/evidence schemas | NEF-T009 | injection, secret, malformed response, outage, stale pricing |
| Findings ledger | VIII | NEF-001 FR-016-FR-017, NEF-006 FR-010-FR-012 | Finding/disposition schemas | NEF-T005, T009 | duplicate recurrence, hallucinated citation, no auto-promotion |
| Quality checkpoint | VIII, XII | NEF-006 FR-013-FR-015 | Dated dispositions and run IDs | NEF-T010 | insufficient dispositions and under-50% default |
| Retention | II, IX, XI | NEF-001 FR-006-FR-008 | Evidence manifest and retention contract | NEF-T004, T005 | unsupported retention, missing blob, conflicting write |

## Schema coverage

| Schema | Defining requirements | Producer | Consumer | Critical invariants |
|---|---|---|---|---|
| TargetDescriptor 2.0.0 | NEF-002 FR-001, FR-016-FR-019 | pin-target | snapshot builder | immutable mode/selector, tag-ref, peeled SHA, provisional acknowledgement |
| TargetSnapshotManifest 2.0.0 | NEF-002 FR-005, FR-017-FR-021 | pin-target | discovery, campaign request | evidence/baseline class, binding state, provenance, digests, environment, consulted paths |
| TargetCapabilityManifest | NEF-002 FR-006-FR-008, FR-014 | capability discovery | orchestrator, all campaigns | required campaigns and reasoned unavailable skips |
| CampaignRequest | NEF-001 FR-002, FR-009, FR-011 | orchestrator | campaign adapter | identity, budgets, configuration, disposable path |
| CampaignResult | NEF-001 FR-004-FR-006, FR-012 | campaign adapter | aggregator | exact states, pass evidence, case completeness |
| EvidenceManifest | NEF-001 FR-006-FR-008 | isolated publisher | verifier, aggregator | content digests and seal time |
| Finding | NEF-001 FR-010, FR-016-FR-017; NEF-006 FR-010-FR-012 | deterministic campaign/model normalizer | publisher, triage | candidate authority, stable fingerprint, evidence |
| Disposition | NEF-001 FR-016-FR-017; NEF-006 FR-013-FR-015 | human triage | report/checkpoint | actor, time, rationale, evidence, allowed decisions |

All schemas declare draft 2020-12, stable versioned `$id`, closed top-level objects, explicit required fields, and nonnumeric Decimal representations where threshold comparison occurs. `CampaignResult` requires sealed evidence and all-pass cases for a pass; skipped cases require a reason. T003 must add executable semantic-schema conformance beyond T001's syntax and structural checks.

## State consistency analysis

- Canonical states are identical in `AGENTS.md`, `PLANNING.md`, constitution III, NEF-001, public interfaces, and `campaign-result.schema.json`.
- Mutation's killed/survived/timeout/invalid/untested categories are measurements/outcomes normalized into the canonical state vocabulary; they do not create a competing global case-state enum.
- Model `supported`/`suspected` are candidate classifications, not pass/fail states or dispositions.
- Human dispositions are deliberately separate from campaign states.
- Unavailable capability is represented as capability `unavailable` plus campaign `skipped` and a reason; it never becomes pass.

## Trust-boundary analysis

- Pin-target has read-only target access and no provider role.
- Target execution has no provider secret or repository write permission.
- Model audit receives only validated secret-scanned data, executes no target code, and has no repository write permission.
- Aggregation has no target execution and no provider secret.
- Publication consumes validated canonical data and executes no untrusted code.
- No step requires customer data, production traffic, production keys, or a second system under evaluation.
- Host and administrator rewrite limitations remain explicit in the constitution, trust model, retention contract, target profile, and NEF-002.

## Target/capability consistency analysis

- `main`, `HEAD`, branches, aliases, and other mutable refs cannot be recorded selectors. Gate evidence uses an `mN` tag binding; provisional execution uses an acknowledged exact SHA.
- Historical provisional `de8c077...` facts match `SESSION_LOG.md`: T-014 and T-015 available; T-016 and Ed25519 unavailable.
- Current default gate `m0` exposes only target-binding as required; global-chain, T-014, T-015, T-016, and Ed25519 campaigns are reasoned unavailable skips because their implementations and executable fixtures are absent at that SHA.
- T-016 and Ed25519 scenarios are conditional and do not specify missing wire formats, signing bytes, key lifecycle, rotation, or legacy rules.
- RFC 8032/FIPS/`cryptography` are independent references only and cannot activate the target signing campaign.

## 2026-07-12 target-pinning amendment analysis

**Amended artifacts:** AGENTS, PRD, PLANNING, kickoff prompts, constitution 1.1.0, NEF-002, clarifications, TargetDescriptor/TargetSnapshotManifest/CampaignRequest 2.0.0, trust model, source matrix, public interfaces, target profiles, task routing, research register, and schema tests.

**Verdict:** zero unresolved critical inconsistencies after the approved amendment.

- One target-pinning seam owns gate and provisional selection; no parallel registry or selector exists.
- `gate-evidence` requires `mN`, tag-ref SHA, peeled commit SHA, reproducible-baseline class, and a non-moved binding. Numeric milestone order is normative.
- Annotated and lightweight tags share one peel invariant: `resolved_sha == peel(tag_ref_sha)`, with commit peeling as identity.
- Provisional input is an acknowledged SHA, remains replayable, and is excluded from gate scoring by explicit class labels.
- A moved snapshot remains valid violation evidence but CampaignRequest 2.0.0 rejects it.
- The deterministic Finding contract already represents moved-tag candidates; no new finding authority or state was introduced.
- Prior-snapshot deletion can evade movement detection. The trust model names append-only/hash-chained snapshot history as a T004/T005 seam without claiming it exists.
- Current gate facts are internally consistent: only `m0`; tag-ref `8362f666...`; peeled commit `cb1d0ba...`; `m1` absent; m0 has target-binding evidence but no executable NEST hash-chain/T-014-T-016/Ed25519 surface.
- Historical `de8c077...` and `1e98933...` records are retained as provisional/non-gate evidence rather than rewritten or promoted.

| ID | Severity | Finding | Resolution |
|---|---|---|---|
| A-018 | Critical | Exact-SHA execution still allowed a moving ref to define a scored campaign and did not distinguish gate evidence. | Resolved by immutable gate/provisional selectors and explicit evidence/baseline classes. |
| A-019 | Critical | A force-moved milestone tag could silently retarget later runs. | Resolved by immutable prior binding comparison, moved violation evidence, campaign refusal, and deterministic candidate finding. |
| A-020 | High | Annotated-only peeling would falsely reject lightweight gate tags. | Resolved by identity peeling for commit refs plus annotated/lightweight fixtures. |
| A-021 | High | Missing gate tags could silently route to current main/provisional work. | Resolved: no automatic fallback; provisional mode requires explicit acknowledgement. |
| A-022 | High | Deleting prior binding history defeats moved-tag comparison. | Residual recorded honestly; append-only/hash-chained snapshot history is assigned to T004/T005 and not claimed in T002. |

## Research consistency analysis

- GitHub retention is conditional on private-repository and organization/enterprise settings; no permanent-storage claim remains.
- Scheduled workflows may be delayed/dropped; manual dispatch and a best-effort watchdog are required.
- OpenAI project budgets are soft thresholds; the application reservation ledger provides the skip decision.
- Hypothesis databases/blobs are version-bound caches/supplements; durable minimized examples are primary.
- No model snapshot, price, mutation tool, or dependency version is prematurely frozen in T001.

## Findings table

| ID | Severity | Finding | Resolution |
|---|---|---|---|
| A-001 | Critical | A pass could have been schema-valid with no cases. | Resolved: pass requires at least one case and every case state pass; implementation must also enforce required-case completeness. |
| A-002 | High | An unavailable capability record could omit its reason. | Resolved: capability schema conditionally requires nonempty reason and evidence. |
| A-003 | High | Announced T-016/Ed25519 behavior could be mistaken for current target behavior. | Resolved: source matrix and specs require normative + implementation + executable evidence at one SHA; initial cases are visible skips. |
| A-004 | High | Provider budgets could be presented as spending caps. | Resolved: research register and NEF-006 define soft alerts plus application reservation. |
| A-005 | Medium | Mutation-specific outcomes might be confused with global case states. | Resolved: they are complete-denominator measurements normalized to canonical states; no global enum expansion. |
| A-006 | Medium | Bootstrap has no NEF commit SHA. | Resolved honestly in snapshot as unavailable-unborn; no fabricated SHA. First checkpoint creates the initial NEF commit. |
| A-007 | Medium | `.targets/` is untracked before scaffold `.gitignore`. | Accepted temporary risk: never stage it; NEF-T002 owns `.gitignore`. |
| A-008 | Low | Semantic JSON Schema validation tool is not installed. | T001 uses standard-library JSON syntax/structural checks; T003 implements executable schema conformance without adding an unapproved T001 dependency. |
| A-009 | Critical | `CampaignRequest` prose required the target manifests but the first schema draft carried only their digests. | Resolved: the schema now requires both embedded validated manifests and their canonical digests. |
| A-010 | High | The first snapshot schema draft used `nef_revision`, conflicting with the approved `nef_sha` public contract and recorded manifest. | Resolved: the normative field is `nef_sha`, with an explicit unavailable-bootstrap alternative. |
| A-011 | Critical | Decimal measurement strings matched both the Decimal and generic-string branches of `oneOf`, making valid Decimal strings invalid. | Resolved: heterogeneous measurements use `anyOf`; floats remain excluded. |
| A-012 | Critical | A pass could contain cases with no evidence digests, and a skipped campaign could contain non-skipped cases. | Resolved: pass cases require evidence and `pass`; skipped campaign cases require a reason and `skipped`. |
| A-013 | High | Repository URLs, workspace paths, and evidence paths could carry credentials or traversal-shaped values. | Resolved: schema patterns refuse URL userinfo, path traversal, and workspaces outside the exact-SHA target root. |
| A-014 | High | Human dispositions could omit all evidence references despite the public contract. | Resolved: disposition evidence digests require at least one entry. |
| A-015 | High | NEF-002 retained the stale `nef_revision` field name after the schema was aligned to `nef_sha`. | Resolved: specification and schema now use `nef_sha`. |
| A-016 | Critical | Mutation-specific outcomes were listed without a deterministic mapping to the six canonical case states. | Resolved: killed/pass, survived/fail, timeout/inconclusive, invalid/invalid, and untested/skipped; campaign infrastructure failures are error. |
| A-017 | High | Missing performance reference and model secret/outage paths allowed ambiguous alternative states. | Resolved: exact state mappings now distinguish reasoned skip, insufficient evidence, invalid input, and infrastructure error. |

All critical/high findings were resolved within the approved plan. Accepted medium/low items are explicitly routed and do not make an unsupported success claim.

## Orphan and duplication checks

- Every PRD core feature maps to at least one specification and task.
- Every spec has functional requirements, acceptance scenarios, sabotage obligations, and success criteria.
- Every normative schema has defining requirements and named producer/consumer.
- Every later v1 goal task T002-T010 has a specification dependency or deferred research point.
- Shared vocabulary lives in NEF-001/public interfaces; other specs reference rather than redefine aggregation or authority.
- No later-work T011-T013 feature was pulled into v1 implementation.

## Final analyze result

NEF-T001 has zero unresolved critical inconsistencies. Remaining missing evidence is capability- or task-time evidence explicitly represented as unavailable, skipped, deferred, or a later hard-stop decision; none is counted as pass.
