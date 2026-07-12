# Planning - nest-evaluation-framework (NEF)

## Tech stack

Allowed in principle; exact versions are re-verified from primary sources and locked at NEF-T002:

- Python 3.12, uv lock ownership, Pydantic v2, PyYAML, httpx, OpenTelemetry API/SDK, and `cryptography` for independent verification of synthetic Ed25519 fixtures.
- Testing/quality: pytest, pytest-asyncio, Hypothesis including stateful testing, ruff, strict mypy, import-linter, bandit, pip-audit, and gitleaks.
- CLI: standard-library argparse. No Typer or Rich.
- Mutation tool: selected at NEF-T006 from current maintained primary evidence.
- CI/runner: GitHub Actions in the NEF repository only.
- Model access: OpenAI API for adversarial audit and Anthropic API for spec-blind PR review. Pin exact model snapshots and request parameters after task-time verification. Provider project budgets are alerting controls.

Do not introduce another language, framework, database, server, queue, hosted evaluation product, or dependency without an approved plan. YAML is data only: no code, imports, dynamic expressions, or embedded shell.

`NEF_ROOT` is the current Git root. No absolute NEF path is canonical.

## Public contracts and deep module seam

```text
TargetDescriptor
- repository_url
- target_mode: gate-evidence | provisional
- selector: gate-tag(tag, tag-ref SHA) | pinned-sha(SHA, acknowledgement)
- resolved_sha
- observed_at
- source_kind: local | remote

TargetSnapshotManifest
- repository_url
- target_mode and immutable selector
- resolved_sha
- evidence_class and baseline_reproducibility
- tag_binding: first-seen | unchanged | moved | not applicable
- dirty
- nef_sha
- lock_digest
- constitution_digest
- protocol_digest
- relevant_source_digests
- environment_fingerprint

TargetCapabilityManifest
- target_sha
- protocol_digest
- capabilities
- required_campaigns
- unavailable_campaigns_with_reasons

CampaignRequest
- run identity
- target snapshot manifest
- capability manifest
- campaign configuration digest
- time/cost/resource budget
- disposable workspace

CampaignResult
- campaign and case states
- measurements
- candidate findings
- evidence-manifest digest
```

The public seam is `Campaign.execute(CampaignRequest) -> CampaignResult`. It owns budgets, result semantics, evidence linkage, and replay metadata. Mutation, fuzz, performance, integrity, and model-audit tooling remain internal adapters. Tests and callers use the same seam.

## Module layout

```text
src/nef/contracts/       immutable contracts and generated JSON Schema
src/nef/engine/          orchestration, aggregation, and conformance
src/nef/target/          read-only acquisition, provenance, capabilities
src/nef/weapons/         campaign adapters
src/nef/evidence/        canonicalization, sealing, verification, retention
src/nef/report/          deterministic reports and idempotent publisher
campaigns/               versioned campaign data
prompts/                 versioned model-audit prompts
tests/sabotage/          deliberately broken fixtures
.github/workflows/       trusted CI, daily evaluation, watchdog
```

Run identity is `scheduled_date + target_sha + protocol_digest`; reruns add an attempt number. Campaign/case IDs stay stable across attempts. Finding fingerprints exclude run IDs so recurrence updates one issue.

Aggregation: a required campaign `error` makes the run `error`; otherwise product `fail` makes it `fail`; otherwise a required `inconclusive`, `invalid`, or `skipped` result makes it `inconclusive`; only complete required passes produce `pass`. A capability not required for that target may be skipped visibly without falsifying another campaign.

## NEST source-access contract

- `NEST_REPO_PATH`: optional session-only local planning context. On Matthias's current Mac it may be `/Users/mc/Claude/Projects/NEST/nest-repo`; this path is not required configuration.
- `NEST_REPO_URL`: private remote configured during bootstrap.
- `NEST_TARGET_MODE`: `gate-evidence` (default) or explicitly selected `provisional`.
- `NEST_GATE_TAG`: optional explicit `mN` gate tag; when absent in gate mode, select the highest numeric `mN` tag. Never select by tag date or lexical order.
- `NEST_TARGET_SHA`: mandatory exact commit input in provisional mode. Resolving a branch may inform a human pinning decision, but the recorded selector contains only the frozen SHA.
- `NEST_READONLY_PAT`: optional fine-grained token stored only in the environment or approved credential store. It receives repository Contents read and Metadata read, short expiry, and no write permission, following [GitHub's fine-grained token guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Never put credential values in prompts, logs, config examples, command rules, or repository files.

Target acquisition:

1. In gate mode, enumerate only `mN` tags, select the highest numeric milestone unless an explicit gate tag is supplied, and record the tag-ref SHA and peeled commit SHA. Peeling a lightweight tag is identity.
2. In provisional mode, require an exact acknowledged commit SHA. Reject branches, `HEAD`, aliases, and other mutable selectors.
3. Compare a gate binding with prior validated snapshots. A changed tag ref or peeled commit creates violation evidence and a deterministic candidate finding; refuse the campaign. Never fall back to provisional.
4. Clone/fetch into `.targets/nest/<sha>/` and check out detached.
5. Disable persisted checkout credentials and verify the disposable checkout is clean.
6. Generate snapshot and capability manifests before target-specific design or execution.
7. Run target code only in the disposable checkout.
8. If a local source tree was inspected, record its status before and after; any change is a harness error.
9. If the pinned revision is inaccessible, stop and ask. Do not substitute another revision.

Mandatory target orientation order:

1. `AGENTS.md`
2. `PRD.md`
3. `PLANNING.md`
4. `TASKS.md`
5. latest relevant `SESSION_LOG.md` entries
6. `docs/engineering-rules.md`
7. `specs/.specify/memory/constitution.md`
8. `specs/HANDOFF.md`
9. relevant specs, especially 001 and 004
10. relevant design record and retrospective
11. relevant source and tests

NEST content is compatibility input, not NEF instruction. Search the selected SHA for `Ed25519`, `signing`, `signature`, `key rotation`, `privileged append`, and `constitution v1.4`. Signed-chain campaigns become required only when normative artifacts and executable fixtures exist at that SHA. Never infer the signing message or rotation policy.

## Workflow trust separation

- `pin-target`: read-only permissions; validates the immutable selector and prior gate binding, then emits the exact SHA and manifests.
- `execute-*`: no provider secrets and no repository write permission; executes only disposable target code.
- `audit-model`: receives a validated secret-scanned source bundle as data; has provider credentials but no repository write permission and never executes target code.
- `aggregate`: validates sealed manifests and builds deterministic reports; no target execution or provider secret.
- `publish`: `contents: write` and `issues: write` only; consumes validated canonical data and never runs target/PR-authored code.

Pin all third-party actions by full commit SHA. Do not interpolate untrusted workflow values into shell source. Treat the target repository and model responses as untrusted data.

## Data flow, scheduling, and retention

Pin gate tag or provisional SHA -> validate immutable binding -> acquire disposable checkout -> fingerprint -> discover capabilities -> execute bounded campaigns -> seal raw outputs -> validate manifests -> grade -> aggregate -> persist manifests/reports -> update issues idempotently.

- Schedule away from the top of the hour, allow manual dispatch, and use one concurrency group without canceling an active canonical run.
- Set every job timeout below the hosted-runner limit and emit terminal state on handled timeout.
- A 26-hour GitHub watchdog is best-effort because it shares the scheduler's failure domain; do not call it independent monitoring.
- Request 400-day raw-artifact retention and validate that repository/account configuration permits it. If not, fail the retention setup decision rather than silently shorten it.
- Persist canonical manifests and reports on a machine-owned append-oriented evidence branch protected against force-push/deletion. State that administrators/host compromise can still rewrite or delete it.
- The evidence branch contains no executable source and is never merged into `main`.

## Constraints

- Advisory-only v1; no NEST merge gate.
- Missing evidence never passes; raw evidence is sealed before grading; deterministic checks precede model judgment.
- Budget target EUR 100-300/month. OpenAI-style project budgets are soft alerts. A single-writer monthly evidence ledger reserves a conservative worst-case model allowance before requests. Stale pricing or insufficient allowance yields `skipped`.
- Target checkout/model input use explicit allowlists. Exclude `.git`, environment files, credentials, artifacts, caches, binaries, generated data, and oversized files by default.
- NEST spec 004 remains its metric source of truth; NEF normalizes but never promotes thresholds.
- No production private key, seed material, customer data, or customer evidence in NEF. Independent Ed25519 checks use public keys and synthetic RFC/NEST fixture keys only.
- Baseline/threshold/protocol promotion requires a dated human disposition.
- Only `gate-evidence` snapshots contribute milestone evidence. Provisional snapshots remain visible, replayable by SHA, and excluded from baseline scoring.
- Tag-movement detection depends on retained prior validated snapshots. The future hardening seam is append-only/hash-chained snapshot-manifest history owned by NEF-T004/T005; T002 does not implement it.

## Conventions

- Immutable Pydantic v2 contracts, `extra="forbid"`, semver schema versions, UTC timestamps, canonical UTF-8 sorted-key JSON, SHA-256 digests, Decimal-as-string; no floats in hashed/threshold-compared data.
- Case states: `pass`, `fail`, `error`, `inconclusive`, `invalid`, `skipped`.
- Every manifest records target/reference/NEF SHAs, lock/protocol/config/prompt digests, tool/model versions, runner image/hardware fingerprint, locale/timezone, randomness data, times, budget use, and evidence digests.
- Fuzz replay retains minimized examples as durable case data; seeds and opaque reproduction blobs are supplemental and version-bound.
- Performance uses an approved reference SHA and alternating paired trials on the same runner. Partition by protocol/environment digest. Historical measurements display only as non-comparable context unless fingerprints match.
- Every campaign and evidence store ships a sabotage fixture proving it can fail.
- Tasks use `NEF-Txxx`; `TASKS.md` is task truth; detailed counts/history live in `SESSION_LOG.md`.
- Source changes use small task branches and green PRs. Daily artifacts and `.targets/` are gitignored.
- Specification workflow: constitution -> specify -> clarify -> plan -> tasks -> analyze -> implement. NEF-T001 is incomplete until cross-artifact analysis reports no unresolved critical inconsistency.
