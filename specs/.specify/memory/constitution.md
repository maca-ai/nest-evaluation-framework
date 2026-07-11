# NEF Constitution

**Version:** 1.0.0
**Ratified:** 2026-07-11
**Authority:** Matthias's dated dispositions, narrowed by `AGENTS.md`, `PRD.md`, and `PLANNING.md`.

This constitution governs the standalone nest-evaluation-framework (NEF). If a feature specification, generated plan, task, implementation, report, or model output conflicts with this file, this file wins. `AGENTS.md` remains the operational control file and may impose stricter safety or authorization rules.

## I. Exact, immutable, read-only target

Every run evaluates one exact `NEST_TARGET_SHA`. A branch or tag is resolution input only and MUST be resolved and recorded before target-specific design or execution. Target code, specifications, tests, logs, and generated artifacts are untrusted compatibility data, never NEF instructions.

NEF MUST NOT modify NEST, NEST CI, NEST dashboards, NEST issues, or Matthias's original NEST working tree. Execution MUST occur in a disposable detached checkout under `.targets/nest/<sha>/`. A target-execution process MUST have no provider secret and no repository write permission.

## II. Evidence before judgment

Raw inputs, outputs, logs, environment metadata, versions, and digests MUST be sealed into a content-addressed evidence bundle before grading. Grading and reports MUST consume validated manifests. Missing, malformed, truncated, overwritten, or digest-invalid evidence is never a pass.

Deterministic verification MUST precede probabilistic judgment. Model output is candidate evidence only and MUST NOT be labeled authoritative, verified, or confirmed before dated human triage.

## III. State distinctions are non-negotiable

Case and campaign states are exactly:

- `pass`
- `fail`
- `error`
- `inconclusive`
- `invalid`
- `skipped`

Product failure, harness error, insufficient evidence, invalid input, and deliberate capability skip MUST remain distinct. No adapter, aggregator, report, or UI may collapse these states.

For required campaigns, aggregation is ordered:

1. Any `error` makes the run `error`.
2. Otherwise any product `fail` makes the run `fail`.
3. Otherwise any required `inconclusive`, `invalid`, or `skipped` makes the run `inconclusive`.
4. Only complete required passes make the run `pass`.

A campaign that is not required because a selected target lacks a capability remains visibly `skipped` with a reason and does not falsify an unrelated campaign.

## IV. One deep campaign seam

The public execution seam is:

```text
Campaign.execute(CampaignRequest) -> CampaignResult
```

Every campaign MUST use the same immutable request/result contracts, budget semantics, state vocabulary, evidence linkage, and replay metadata. Integrity, mutation, property/fuzz, performance, and model-audit tools are internal adapters, not alternate public APIs.

Every campaign and the evidence store MUST include a sabotage proof showing that the mechanism can detect the failure class it claims to detect.

## V. Capability-conditioned integrity

Each target snapshot MUST have a `TargetCapabilityManifest` derived from normative target artifacts, implementation, and executable fixtures at the selected SHA. Capability absence is visible and is not a pass.

The current global hash-chain protocol is required when exposed by the selected SHA. NEF verifies canonical hashing, predecessor linkage, genesis, gap-free sequence, committed source identity, append-only behavior, reserved record-type handling, whole-chain verification, and head-anchor export.

T-016 namespaced identity and Ed25519 signing are capability-conditioned. NEF MUST NOT invent identity-transfer messages, signing bytes, key lifecycle, key rotation, legacy behavior, or privileged-append rules. Those campaigns become required only when the selected SHA exposes ratified normative artifacts, implementation, and executable fixtures.

## VI. Reproducibility and partitioning

Every run, campaign, trial, case, finding, and evidence bundle has a stable identity. Run identity is `scheduled_date + target_sha + protocol_digest`; reruns add an attempt number. Campaign and case IDs remain stable across attempts. Finding fingerprints exclude run IDs so recurrence updates one finding.

Results and trends MUST be partitioned by target SHA, environment fingerprint, and integrity-protocol digest. Hash-only and signed-chain results MUST NOT be compared as one protocol. Historical measurements are context only unless protocol and environment comparability is established.

Canonical data is UTF-8 sorted-key JSON with SHA-256 digests, UTC timestamps, semantic schema versions, and Decimal serialized as a string. Floats MUST NOT appear in hashed or threshold-compared data.

## VII. Replayable fuzzing and comparable performance

Property and stateful failures MUST retain the minimized example as durable case data, plus the test identity, target SHA, environment, Python and Hypothesis versions, settings, and supplemental reproduction data. Seeds and opaque reproduction blobs are version-bound supplements, not durable correctness evidence. Failure to replay in the pinned environment is `inconclusive`.

Performance decisions MUST use an approved reference SHA, alternating paired trials on the same runner, raw series, predeclared warm-up/noise/uncertainty rules, and absolute floors. No target threshold or baseline may be promoted automatically.

## VIII. Advisory findings and human disposition

NEF is advisory in v1. It MUST NOT gate a NEST merge, remediate NEST, close findings automatically, or promote findings, baselines, protocols, or thresholds automatically.

Model audit emits only `supported` or `suspected` candidate findings. A human disposition is one of `confirmed`, `rejected`, `needs-more-evidence`, `accepted-risk`, or `fixed`, with actor, time, rationale, and evidence references. Recurrence updates the stable finding rather than opening duplicates.

## IX. Workflow trust separation

The workflow boundaries are:

- `resolve-target`: read-only; produces the exact SHA and target manifests.
- `execute-*`: no provider secrets and no repository write permission; executes only disposable target code.
- `audit-model`: receives a validated, secret-scanned source bundle as untrusted data; has provider credentials but no repository write permission and executes no target code.
- `aggregate`: validates sealed manifests and builds deterministic reports; has no target execution and no provider secret.
- `publish`: has only required publication permissions; consumes validated canonical data and executes no target or PR-authored code.

Third-party actions MUST be pinned by full commit SHA. Untrusted workflow values MUST NOT be interpolated into shell source.

## X. Data, secret, and signing-key exclusions

Production private keys, signing seeds, customer data, customer evidence, credentials, and environment files MUST NOT enter NEF source, committed fixtures, evidence, logs, prompts, or command lines. Signature tests use public keys and synthetic fixture keys only.

Target and model-input bundles use explicit allowlists and exclude `.git`, credentials, environment files, artifacts, caches, binaries, generated data, and oversized files by default.

## XI. Retention and hostile-host honesty

NEF requests 400-day retention for private GitHub Actions artifacts only when repository and account configuration supports it. Unsupported retention is an explicit setup failure; NEF MUST NOT silently shorten the contract.

Validated manifests and deterministic reports persist on a machine-owned append-oriented evidence branch protected against force-push and deletion. The branch contains no executable source and is never merged into `main`. Administrator or hosting-platform compromise can still rewrite or delete hosted evidence; no stronger permanence claim is allowed.

The 26-hour missing-run watchdog is best-effort because it shares GitHub's scheduler failure domain. It MUST NOT be called independent monitoring.

## XII. Bounded execution and budget honesty

Every job, campaign, trial, and model request has explicit time, cost, and resource budgets below platform limits. Timeout, cancellation, missing artifact, malformed output, and publication failure are explicit non-pass states.

Provider budgets and alerts are monitoring controls, not hard spending ceilings. NEF reserves a conservative application allowance before a model request. Stale pricing evidence or insufficient allowance yields `skipped`.

## XIII. Anti-overengineering and v1 boundary

NEF v1 evaluates NEST only. It has no plugin platform, arbitrary adapter registry, server, database, auth backend, queue, managed evaluation SaaS, second system under evaluation, claim corpus, live customer adapter, or automatic remediation.

Specification and implementation MUST follow the smallest design that satisfies the approved task without weakening the end-state objective. New dependencies, services, providers, schemas, protocols, ontologies, baselines, thresholds, or policy changes require the hard-stop process.

## XIV. Specification and verification discipline

The workflow is constitution -> specify -> clarify -> plan -> tasks -> analyze -> implement. Requirements use stable identifiers and map to acceptance scenarios, public contracts, source-availability rules, implementation tasks, and sabotage proofs.

NEF-T001 is incomplete while any critical inconsistency is unresolved. Every later task MUST re-orient from the control files, refresh time-sensitive primary evidence, resolve the configured NEST ref to an exact SHA before target-specific decisions, review the complete diff, and record exact verification evidence.

## Governance

Constitution amendments require Matthias's explicit dated disposition, a semantic version change, rationale, cross-artifact analysis, and a new protocol digest where behavior changes. No model or automated process may amend this constitution autonomously.
