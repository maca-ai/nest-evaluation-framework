# Tasks - nest-evaluation-framework (NEF)

Rules: take the top unchecked Pending task whose dependencies are met. One task may be In progress. One task equals one branch, reviewable diff, verification record, and session-log entry. Goal mode covers NEF-T001 through NEF-T010 only.

## Done

- [x] NEF-T000 Control package audited and hardened (2026-07-11): advisory daily evaluator, exact-SHA target contract, five campaign classes, evidence-first ordering, secure job separation, bounded goal autonomy, and restart-safe kickoff package approved.
- [x] NEF-T001 Constitution and executable specifications (2026-07-11): completed as the explicitly authorized repository genesis; constitution, executable specifications, normative schemas, target capability profile, and cross-artifact analysis landed together because no pre-T001 baseline existed. Branch, draft-PR, CI, and review discipline is mandatory from NEF-T002 onward.

## In progress

- [ ] **NEF-T002 Reproducible scaffold and trusted CI.** Implementation, local verification, and local checkpoint commits complete on `feat/NEF-T002-reproducible-scaffold`; push, draft PR, GitHub CI/review, and merge approval remain. Scope: Python 3.12/uv lock, module skeleton, deterministic quality/security CI, trusted-base advisory Anthropic spec-blind reviewer, RFC 8032 known-answer coverage, constitution 1.1.0 plus target-pinning contract 2.0.0 amendment, Draft 2020-12 immutable-target vectors, and m0 gate/provisional target profiles.

## Pending - v1 goal

- [ ] **NEF-T003 Contracts and deep campaign interface.** Implement target/run/campaign/case/finding/evidence contracts, including TargetDescriptor/TargetSnapshotManifest/CampaignRequest 2.0.0 cross-field invariants (`pinned_sha == resolved_sha`, `resolved_sha == peel(tag_ref_sha)`), generated schemas, aggregation, `Campaign.execute`, deterministic fake, argparse CLI, and shared conformance suite. Sabotage every non-pass, moved-binding request, and missing-evidence state.
- [ ] **NEF-T004 Evidence store and offline verifier.** Canonical JSON, content addressing, atomic create-without-overwrite, digest-verified reads, sealed-before-graded bundles, 400-day retention metadata, evidence-branch layout, and `nef verify`. Test tamper, truncation, duplicate write, malformed manifest, and missing blob. Provide the append-only storage substrate for the later hash-chained snapshot-binding-history seam; do not claim moved-tag durability until T005 integrates it.
- [ ] **NEF-T005 Secure target orchestration, integrity campaign, and publication.** Immutable target pinning/acquisition, numeric highest-`mN` default, annotated/lightweight peeling, explicit provisional SHA mode, no fallback, prior validated binding comparison, moved-tag refusal plus deterministic finding, snapshot-history hardening over T004 storage, capability discovery, current hash-chain conformance, future signed-chain conformance, off-hour schedule, manual dispatch, best-effort watchdog, concurrency/idempotency, target suite baseline, aggregation, evidence publisher, and stable GitHub Issue fingerprints. Prove trust separation and sabotage numeric ordering, missing gate, moved tag-ref/peeled commit, prior-history deletion, product/harness/missing-run/rerun/duplicate-finding paths.
- [ ] **NEF-T006 Weapon A - mutation.** Select and lock a maintained tool from current primary evidence; explicit inclusion manifest; disposable worktrees; bounded shards; full killed/survived/timeout/invalid/untested denominator; target chain/signature verification paths when capability exists; survivor evidence and sabotage proof.
- [ ] **NEF-T007 Weapon B - property and stateful fuzzing.** Campaign available target surfaces; retain minimized example/test identity/Hypothesis version/reproduction data/environment; clean pinned replay. Cover identity transfer and signature parsing/verification when available. Future unavailable surfaces remain explicit skips.
- [ ] **NEF-T008 Weapon C - performance.** Approved reference registry; alternating paired trials; raw series; warm-up/uncertainty/noise rules; environment fingerprint; absolute floors; human-only promotion. Partition by protocol digest and measure signing/verification overhead only against a comparable reference. Detect a controlled slowdown.
- [ ] **NEF-T009 Weapon D - adversarial model audit.** Source allowlist/secret scan/size-bound manifest; prompt-injection treatment; pinned OpenAI snapshot/request/schema/SDK; conservative allowance reservation; raw-response sealing; `supported`/`suspected` candidates; integrity-claim honesty. No target execution or GitHub write. Test malformed response, outage, exhausted budget, stale pricing, and planted defect.
- [ ] **NEF-T010 Model-audit quality checkpoint.** Schedule for 14 days after first successful Weapon D run; compare supported candidates with dated dispositions. Default under 50% confirmed means weekly cadence and fuzz allowance reallocation. Threshold change requires Matthias and a new protocol digest.

An unavailable Ed25519 surface is a visible capability skip. It does not block earlier hash-chain evaluation and is never counted as a pass.

## Later work - outside first goal

- [ ] **NEF-T011 Claim corpus.** Versioned claim/case/metric/profile loaders, balanced cases/reference solutions, source mapping, and digest-drift invalidation pending human review.
- [ ] **NEF-T012 NEST adapters and replay.** Recorded-artifact normalization and disposable compose target; blocked until NEST exposes required runnable targets. Prove read-only behavior/replay equivalence.
- [ ] **NEF-T013 Static scorecard.** Canonical JSON and self-contained HTML from validated manifests only; trends partitioned by protocol/environment digest; corrupted/missing evidence produces an incomplete scorecard.
