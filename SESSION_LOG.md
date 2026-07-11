# Session Log — nest-evaluation-framework (NEF)

## 2026-07-10 — five-file package + full-build amendment

**Date:** 2026-07-10

**Goal of the session:** Convert the approved NEF standalone specification into the five-file system and record the dated amendment that supersedes the post-T-073 deferral.

**Files changed:** AGENTS.md, CLAUDE.md, PRD.md, PLANNING.md, TASKS.md, SESSION_LOG.md (all created).

**Decisions / bugs encountered:**
- AMENDMENT (Matthias, 2026-07-10): full build starts NOW. Stated goal: a framework that runs once daily against the whole nest-repo and tries to break it, so NEST reaches production super-stable, resilient, smooth, fast, reliable. v1 center = daily breaker; claim corpus and live adapters move to later milestones.
- Ratified: runner = GitHub Actions cron in this repo with read-only clone of nest-repo (nest-audit-readonly PAT pattern; zero NEST CI changes); red policy = ADVISORY + TRIAGE (report → adversarial triage → dated dispositions; never blocks NEST merges); all four weapon classes in v1 (mutation, fuzz/property, perf/load regression, automated daily Sol audit); budget €100–300/mo with capped provider projects (~€150 OpenAI, ~€100 Anthropic, ~€40 Actions minutes; 80% alerts).
- Consequences: NEF needs a PRIVATE GitHub remote (stays private until NEST trademark rename clearance); Sol builds ⇒ the spec-blind CI reviewer for this repo is ANTHROPIC (cross-vendor flip of the nest-repo pattern).
- Sol-audit quality checkpoint baked in as NEF-T008, due 2026-07-24: <50% triage survival of VERIFIED findings ⇒ cadence drops to weekly. This was previously only advice in chat; now it is a dated task.
- Load-bearing citations behind the design were verified fresh 2026-07-10: OpenAI hosted Evals shutdown 2026-11-30 (own portable local specs), Anthropic agent-eval guidance (deterministic-first, capability vs regression), REFLECT arXiv:2605.19196 (no judge gating in v1), NIST probes + NIST AI 800-3 (faithfulness/completeness/sufficiency; fixed-corpus estimand with Wilson intervals), GitHub Spec Kit flow.
- Standing invariants: NEF never writes to nest-repo; missing evidence never passes; product failure / harness error / insufficient evidence / invalid case stay distinct; NEST spec 004 = metric source of truth; NEST 004 SC-004 thresholds promote only via NEST T-071 human ratification.
- Repo location corrected from Desktop to /Users/mc/Claude/Projects/NEST/nest-evaluation-framework.

**Next steps for whoever picks up next:**
1. Matthias: copy these five files (+ CLAUDE.md) to the repo root at /Users/mc/Claude/Projects/NEST/nest-evaluation-framework, `git init`, one initial commit, create PRIVATE GitHub repo, push, add secrets (NEST_READONLY_PAT, OPENAI_API_KEY capped project, ANTHROPIC_API_KEY capped project).
2. Builder (Sol, Codex desktop app): orient per AGENTS.md read-first directive, then plan NEF-T001 (constitution + feature specs) and wait for approval. One task at a time.
3. Do not let NEF sessions displace the remaining Fable-window NEST items (retro chore PR, T-016, first manual Sol audit — which doubles as the proving run for weapon D, so run it FIRST — and the V-001 Fri-El ask).

**Supersession note (2026-07-11):** This entry is retained verbatim as history. The amendment below supersedes its path, task ordering, evidence persistence, provider-cap, model-label, fixed-checkpoint, and kickoff assumptions.

## 2026-07-11 - build-plan brittleness review and export-package amendment

**Goal:** Harden the six control files, add a restart-safe kickoff prompt, and package them for a new standalone Codex workspace without copying or modifying NEST.

**Package files:** AGENTS.md, CLAUDE.md, PRD.md, PLANNING.md, TASKS.md, SESSION_LOG.md, build-kickoff-prompt.md.

**Matthias decisions:**

- Codex uses bounded goal autonomy for NEF-T001 through NEF-T010. Hard-stops, scope changes, milestone reviews, inaccessible revisions, and repeated verification failures still require a stop.
- Raw daily evidence requests 400-day private Actions retention; small validated manifests/reports persist on an append-oriented evidence branch.
- The export folder is manually moved to Desktop and becomes its own Git root. NEF uses portable `NEF_ROOT`, not a fixed absolute path.
- The package remains an untracked export while inside NEST and does not change NEST source/control files.

**NEST state and succession:**

- Local GitHub-main snapshot observed 2026-07-11: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`.
- T-014 state projector and T-015 ingestion gate are merged in that snapshot; T-016 is namespaced identity.
- Matthias's dated disposition: T-016 is actively being built in tmux on the VPS. The VPS may be ahead of GitHub main.
- Ed25519 per-record signing and constitution v1.4.0 are the next announced NEST integrity track; they are not claimed implemented on the packaged snapshot.
- NEF must resolve/record exact target SHAs. For unmerged VPS work, it requests an accessible branch or SHA and never guesses or silently falls back.
- NEST source/specs are not copied or symlinked into this package. Development may inspect an optional read-only local path; execution uses a disposable detached checkout.

**Brittleness corrected:**

- GitHub schedule is not delivery proof; add manual dispatch, bounded jobs, idempotent attempts, and a best-effort 26-hour missing-run watchdog.
- An ephemeral local evidence store is not durable; evidence contracts/persistence precede weapon implementation.
- Shared contracts/engine now precede every weapon and expose one deep campaign interface.
- Hypothesis seeds alone are not durable replay; retain minimized example, versions, reproduction data, target SHA, and environment.
- Historical VPS performance is not directly compared with hosted-runner measurements; use paired comparable trials and protocol partitions.
- Provider project budgets are soft alerts; NEF reserves a conservative application allowance and skips when evidence/allowance is insufficient.
- Model output no longer uses authoritative labels; it emits supported/suspected candidates for triage.
- Target execution, provider secrets, and GitHub write permission are separated.
- Findings use stable fingerprints and idempotent issue updates.
- The model-audit checkpoint is first successful audit plus 14 days, not a fixed calendar date.
- Current hash-chain and future signed-chain results are separated by integrity-protocol digest.

**Primary evidence checked 2026-07-11:**

- GitHub Actions scheduling, runner limits, retention, least privilege, full-SHA pinning, and fine-grained read tokens.
- OpenAI project budget behavior and pinned-model guidance.
- Anthropic agent-evaluation guidance on tasks, trials, graders, transcripts, deterministic outcomes, and human calibration.
- Hypothesis replay/database/version guidance; current mutation and Python benchmark documentation.
- GitHub Spec Kit; UK AISI Inspect run logs; EleutherAI reproducibility guidance.
- RFC 8032, NIST FIPS 186-5, and official `cryptography` Ed25519 documentation.

**Next task:** After the folder is moved to Desktop and bootstrapped as its own repository, start NEF-T001. Before target-specific decisions, resolve an accessible NEST ref to an exact SHA and record the target snapshot/capability manifests.

## 2026-07-11 - standalone bootstrap orientation blocked on target configuration

**Observation time:** 2026-07-11T11:00:05Z

**Scope:** Initialize the standalone NEF Git root, verify the seven-file control package, inspect optional local NEST planning context read-only, and resolve the configured remote target before preparing NEF-T001.

**NEF state:**

- Git root initialized at the current workspace root; task branch `codex/nef-t001` created before this journal write.
- The seven approved package files are present and `CLAUDE.md` is exactly `@AGENTS.md` plus one final newline.
- The root also contains an unapproved `.DS_Store`, so the directory does not currently contain exactly only the seven approved files.
- Top eligible Pending task: NEF-T001. Active execution mode: supervised; the prescribed goal has not been started.

**Optional local NEST planning context (not selected as the execution target):**

- Locator: `/Users/mc/Claude/Projects/NEST/nest-repo`.
- Origin observed: `https://github.com/maca-ai/nest.git`.
- Exact local HEAD: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`.
- Branch: `main`.
- Dirty state: clean.
- Action taken: repository metadata inspection only; no tests executed and no files written.

**Target resolution and capability search:**

- `NEST_REPO_PATH`: unset; the documented optional local path above was accessible for planning context.
- `NEST_REPO_URL`: unset.
- `NEST_TARGET_REF`: unset.
- `NEST_TARGET_SHA`: unset.
- Selected target SHA: **MISSING EVIDENCE**.
- Required VPS/T-016 revision accessibility: **MISSING EVIDENCE**; the prior session record says the VPS may be ahead of GitHub `main`.
- Target capability search: not performed because no requested ref could be resolved to an exact selected SHA. The local `main` snapshot was not silently substituted.
- Snapshot fields pending target selection: branch or tag, target dirty state, lock digest, constitution digest/version, integrity-protocol digest, relevant source digests, consulted target paths, and target capability manifest are all **MISSING EVIDENCE**.

**Bootstrap environment fingerprint:** Darwin 23.6.0 arm64; macOS 14.6 (23G80); Git 2.39.5 (Apple Git-154); `LANG=C.UTF-8`; `LC_ALL=C`; observation recorded in UTC.

**Hard stop:** Matthias must provide/configure `NEST_REPO_URL` and `NEST_TARGET_REF`, identifying an accessible branch or exact SHA for the required VPS/T-016 work if that work is the intended target. Do not use `main` by default. After resolution, record the complete target snapshot provenance and capability search before target-specific NEF-T001 design.

## 2026-07-11 - exact-SHA target orientation completed for NEF-T001 planning

**Observation time:** 2026-07-11T12:34:16Z

**Matthias disposition superseding the prior bootstrap hard stop:** Use `https://github.com/maca-ai/nest.git`, requested ref `main`, and accessible baseline `de8c0772dcb1890bfbf7c2c449a4252f63e0807a` for initial NEF-T001 constitution/specification work. Unmerged VPS/T-016 work is not required. T-016 and Ed25519 remain capability-conditioned unavailable cases; their unknown implementation details remain **MISSING EVIDENCE** rather than blocking the versioned capability seam.

### TargetDescriptor

```yaml
repository_url: https://github.com/maca-ai/nest.git
requested_ref: main
resolved_sha: de8c0772dcb1890bfbf7c2c449a4252f63e0807a
observed_at: 2026-07-11T12:34:16Z
source_kind: remote
```

Remote confirmation: read-only `git ls-remote` returned `de8c0772dcb1890bfbf7c2c449a4252f63e0807a` for `refs/heads/main`. The commit subject is `fix(core): Sol audit remediation — B1/B2/B3/C2/C3 (#18)` with commit time `2026-07-10T20:53:33+02:00`.

### TargetSnapshotManifest

```yaml
repository_url: https://github.com/maca-ai/nest.git
requested_ref: main
resolved_sha: de8c0772dcb1890bfbf7c2c449a4252f63e0807a
branch_or_tag: refs/heads/main
checkout_mode: detached
checkout_path: .targets/nest/de8c0772dcb1890bfbf7c2c449a4252f63e0807a
dirty: false
target_tree: f265c07c60deb3921bf2680b1013804aa9cb5cca
nef_sha: unavailable-unborn-repository
lock_digest_sha256: 5b6f7af0cd9f72e75e30a384ba0b95b809544032e91b283513784a6b29494186
constitution_version: 1.3.0
constitution_digest_sha256: 6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a
integrity_protocol_digest_sha256: a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40
environment_fingerprint: Darwin 23.6.0 arm64; macOS 14.6 (23G80); Python 3.9.6 system interpreter; uv 0.11.21 (5aa65dd7a, aarch64-apple-darwin); Docker 28.5.2 (ecc6942); LANG=C.UTF-8; LC_ALL=C
```

`nef_sha` is explicitly unavailable because the newly initialized NEF repository has no commit yet; this bootstrap fact is not represented as a target pass. The disposable checkout has a credential-free origin URL, no checkout-local HTTP extraheader, and no checkout-local credential helper. No tests or campaigns were executed during orientation. The original optional local NEST checkout remained clean before and after inspection at the same SHA.

Protocol-digest construction: SHA-256 of the lexicographically ordered stream of standard `sha256  path` lines for the following protocol-defining files: `docs/design/T-013-event-log.md`, `packages/nest-core/migrations/versions/0001_event_log.py`, `packages/nest-core/src/nest_core/deterministic/hashing.py`, `packages/nest-core/src/nest_core/deterministic/serialization.py`, `packages/nest-core/src/nest_core/eventlog/records.py`, `packages/nest-core/src/nest_core/eventlog/schema.py`, `packages/nest-core/src/nest_core/eventlog/verify.py`, `packages/nest-core/src/nest_core/eventlog/writer.py`, `specs/.specify/memory/constitution.md`, and `specs/001-core-pipeline/spec.md`.

Relevant source digests (SHA-256):

- `specs/001-core-pipeline/spec.md`: `1a095743c37a0c3de7a3db36e9a0e8137aac8c92e7bb73096d0a5421a9d501f1`
- `docs/design/T-013-event-log.md`: `4fb527d099fea9d7de10059afc54329e28e43fd73c4c461b826549d25ba90c39`
- `packages/nest-core/src/nest_core/deterministic/serialization.py`: `6c99ddadfd24ababf67f71b84d6009f9f18f8f6cc8d4b01141bde6623921ff3b`
- `packages/nest-core/src/nest_core/deterministic/hashing.py`: `fcd409c8518466ad0a5e5f8a8cce22ad6de9508fa458949ad4397d39a5aeb3f6`
- `packages/nest-core/src/nest_core/eventlog/records.py`: `45dfc5715e25aa934f9ded5910f11bbea9019beb2b9b959ae95fdf2498801110`
- `packages/nest-core/src/nest_core/eventlog/schema.py`: `dec927b43f2cf73846e2885cd5ec2c0d57765e0ff78d6c0aebebab67b106dc5c`
- `packages/nest-core/src/nest_core/eventlog/writer.py`: `c35124715dbe68e417f6bbbb2f75d869cea5c8cd14ad9e36408aad7f00a25af8`
- `packages/nest-core/src/nest_core/eventlog/verify.py`: `c3f2f8882cbc34a0d458d6ef15862dc82f292a9fb6a3a91ba764092027b79866`
- `packages/nest-core/migrations/versions/0001_event_log.py`: `807804374a90d9599400205e7a5b727843fff93e836eb361898a05680facce3b`
- `packages/nest-core/tests/test_eventlog_hashing.py`: `486d363178575a7dbb6974c0fbbe630db77d0256631862acb63eaab54f2394b5`
- `packages/nest-core/tests/test_eventlog_db.py`: `f4e9cca569e27722ae43460dc4a43d2fd75fc2a301e156488c6e959f6a43f365`
- `packages/nest-core/tests/test_eventlog_permissions.py`: `078123b974be7131f7d6c44fa8b675f7bec33dffab2587e94d64a1d0427410dc`
- `packages/nest-core/tests/test_eventlog_verify_cli.py`: `6fd1a2552a23d50a3f238426076b41ab649cebcd1dfa65ab450402f601ec0bf3`
- `docs/design/T-014-state-projector.md`: `3346232e3a41ae5b6c07773275937df80519472e6eea4546f1fde5ae85dd74dc`
- `packages/nest-core/src/nest_core/deterministic/projection.py`: `be71d7c1079b369dfbe9ed30712c99796bf4eac0d6c257a179adcf028d64f994`
- `packages/nest-core/src/nest_core/projector/runner.py`: `141a05e2419b46fed5cad4378e205ce1c4e19506f0f37a8ab594abc49d10982e`
- `packages/nest-core/migrations/versions/0002_state_projection.py`: `6475b5ead9e987fd085cc439cffab316e982979bbd1ff7a098cd76b9e3e5417c`
- `packages/nest-core/tests/test_projection_fold.py`: `1bcca130aec5a9a066b2b60fbc2870a40fbb24b354a73ebb8283d11d461a6504`
- `packages/nest-core/tests/test_projector_db.py`: `f5829acd8de693e58f3bad3f14973f3f1c9e1fa66091252a19d870992bd28f47`
- `docs/design/T-015-ingestion-gate.md`: `7cd4a5f760a2effda01914dbb16c7529440c648d223643a4dec4f603f2bfbcb6`
- `packages/nest-core/src/nest_core/deterministic/ingestion_gate.py`: `8419d0a7c3463feacdd971cc8e17346666b3bd23cef0c3a85ae8aa6036765124`
- `packages/nest-core/src/nest_core/intake/service.py`: `c502e15613f0084bd7f40b131e898809921931260f5d3251c322952c512fd174`
- `packages/nest-core/tests/test_ingestion_gate.py`: `c03e10479a2fd1f4f69c4fc88a29b89601193bd30035adde1108a4bd63a486bd`
- `packages/nest-core/tests/test_intake_db.py`: `9b8ee0a7f293fe89fe439e3b08d9135a240f1dce617e55e4bee5f7dcef2cfa5a`
- `packages/nest-core/src/nest_core/contracts/identity.py`: `f4c7724f95ad0778948b4782682c41946fd78fd47c9970f81bf8842c3f0f5419`

### TargetCapabilityManifest

```yaml
target_sha: de8c0772dcb1890bfbf7c2c449a4252f63e0807a
protocol_digest: a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40
capabilities:
  global-hash-chain-v1:
    state: available
    evidence: normative specification, design record, migration, source, golden-vector tests, DB tamper tests, permissions tests, and verifier CLI tests
  t-014-state-projector:
    state: available
    evidence: deterministic fold, DB runner, migration 0002, rebuild-byte-identity tests, idempotency/read-your-writes tests, and fail-stop tests
  t-015-ingestion-gate:
    state: available
    evidence: deterministic gate, intake service, recorded decision/quarantine vocabulary, atomicity tests, hostile-input tests, mixed-intake chain verification, and no-gateless-append test
  t-016-namespaced-identity:
    state: unavailable
    evidence: SourceIdentity triple contract exists, but TASKS marks T-016 Pending and no ratified identity-transfer/sensor-replacement implementation or executable fixtures exist
  ed25519-per-record-signing:
    state: unavailable
    evidence: no ratified constitution v1.4.0, signing message, key lifecycle/rotation protocol, implementation, or executable fixture exists at this SHA
required_campaigns:
  - target-integrity/global-hash-chain-v1
unavailable_campaigns_with_reasons:
  - campaign: target-integrity/t-016-namespaced-identity
    state: skipped/unavailable
    reason: selected SHA lacks the ratified T-016 implementation and fixtures; do not invent the interface
  - campaign: target-integrity/ed25519-per-record-signing
    state: skipped/unavailable
    reason: selected SHA is constitution 1.3.0 and lacks the ratified signing protocol, implementation, and fixtures; do not invent signing or key-rotation semantics
```

Current hash-chain behavior found at the selected SHA: canonical UTF-8 sorted-key JSON; SHA-256; one global chain; 32-byte zero genesis; gap-free sequence and sequence position commitment; predecessor linkage; schema version, source triple, times, trace ID, payload, tags, and other stored fields committed into each record hash; full-chain streaming verification; reserved writer-record-type refusal at the writer boundary; separate ingest/correction DB roles; append-only permission matrix; duplicate-receipt evidence; and canonical chain-head anchor export. Honesty boundary retained: without a published external anchor, a privileged actor can rewrite and re-chain history; Ed25519 is not present to close the announced per-record authorization gap.

Capability search terms: `Ed25519`, `signing`, `signature`, `key rotation`, `privileged append`, `constitution v1.4`, `T-014`, `state projector`, `T-015`, `ingestion policy gate`, `T-016`, `namespaced identity`, `identity transfer`, and `sensor replacement`. The only signing-related target hit was the pre-approved `cryptography` dependency description for future hash-chain/record-signing work; other `signature` hits referred to UI or schema-diff wording, not a signing protocol. No Ed25519 implementation or fixture was found.

Consulted target paths, in orientation order: `AGENTS.md`; `PRD.md`; `PLANNING.md`; `TASKS.md`; latest relevant `SESSION_LOG.md` entries; `docs/engineering-rules.md`; `specs/.specify/memory/constitution.md`; `specs/HANDOFF.md`; `specs/001-core-pipeline/spec.md`; `specs/004-replay-eval-harness/spec.md`; `docs/design/T-013-event-log.md`; `docs/design/T-014-state-projector.md`; `docs/design/T-015-ingestion-gate.md`; `packages/nest-core/src/nest_core/contracts/identity.py`; current event-log deterministic/source/migration files; current projector deterministic/source/migration files; current ingestion-gate/intake source files; and their relevant tests listed in the digest register above.

**Disposition:** This capability manifest is current for the exact selected SHA at the observation time. T-014 and T-015 are available. T-016 and Ed25519 are explicit `skipped/unavailable` capability cases, not passes and not blockers to NEF-T001's versioned capability-discovery design. Any future accessible ref is resolved to a new exact SHA and receives a new snapshot/capability manifest before specification amendment.

## 2026-07-11 - NEF-T001 goal-mode implementation plan

**Goal-mode start and target refresh:** Matthias started the exact bounded goal from `AGENTS.md`. At 2026-07-11T12:42:43Z, read-only `git ls-remote https://github.com/maca-ai/nest.git refs/heads/main` again resolved `main` to `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`. The disposable detached checkout remains clean at that SHA; the optional original local NEST checkout also remains clean. The TargetDescriptor, TargetSnapshotManifest, TargetCapabilityManifest, source digests, protocol digest, environment fingerprint, and consulted paths recorded in the immediately preceding entry remain current. No target file was written and no target campaign was executed.

**Task:** NEF-T001 - Constitution and executable specifications. This is the top eligible Pending task and the only task authorized for this implementation session.

**Exact files to create:**

- `specs/.specify/memory/constitution.md`
- `specs/HANDOFF.md`
- `specs/clarifications.md`
- `specs/001-framework-contracts/spec.md`
- `specs/002-target-integrity/spec.md`
- `specs/003-mutation-campaign/spec.md`
- `specs/004-property-fuzz-campaign/spec.md`
- `specs/005-performance-campaign/spec.md`
- `specs/006-adversarial-model-audit/spec.md`
- `specs/001-framework-contracts/contracts/target-descriptor.schema.json`
- `specs/001-framework-contracts/contracts/target-snapshot-manifest.schema.json`
- `specs/001-framework-contracts/contracts/target-capability-manifest.schema.json`
- `specs/001-framework-contracts/contracts/campaign-request.schema.json`
- `specs/001-framework-contracts/contracts/campaign-result.schema.json`
- `specs/001-framework-contracts/contracts/evidence-manifest.schema.json`
- `specs/001-framework-contracts/contracts/finding.schema.json`
- `specs/001-framework-contracts/contracts/disposition.schema.json`
- `docs/research-register.md`
- `docs/trust-model.md`
- `docs/source-availability-matrix.md`
- `docs/retention-contract.md`
- `docs/public-interfaces.md`
- `docs/target-capability-profile.md`
- `docs/cross-artifact-analysis.md`

**Exact existing files to update:** `TASKS.md` and `SESSION_LOG.md` only. `AGENTS.md`, `CLAUDE.md`, `PRD.md`, `PLANNING.md`, `build-kickoff-prompt.md`, all NEST files, and all implementation/workflow/dependency files remain untouched. `.gitignore` remains NEF-T002 scope; `.targets/` must not be staged.

**Specification allocation:** 001 owns shared vocabulary, immutable public contracts, JSON Schemas, evidence-before-grading, aggregation, advisory findings, orchestration, publication, and the `Campaign.execute(CampaignRequest) -> CampaignResult` seam. 002 owns exact-SHA resolution/acquisition, snapshot/capability manifests, current hash-chain conformance, the selected target profile, T-014/T-015 availability, and capability-conditioned T-016/Ed25519 cases. 003 owns mutation. 004 owns property/stateful fuzzing. 005 owns paired performance. 006 owns adversarial model audit and its candidate-finding boundary.

**Public interface/schema decisions:** JSON Schema draft 2020-12; contract version `1.0.0`; closed objects; UTC timestamps; lowercase SHA-256; Decimal-as-string; no floats in hashed or threshold-compared data. Case states remain exactly `pass`, `fail`, `error`, `inconclusive`, `invalid`, `skipped`. The aggregation order remains required `error` -> product `fail` -> required incomplete/non-pass -> `inconclusive` -> complete required passes only -> `pass`. Missing evidence cannot pass. Capability absence is an explicit reasoned skip and never a pass. T003 must implement contracts whose generated schemas semantically conform to these normative schemas.

**Target decisions:** Bind the initial target profile to SHA `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`, constitution 1.3.0, and protocol digest `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`. Require current global hash-chain conformance. Record T-014 and T-015 available. Record T-016 and Ed25519 `skipped/unavailable`; define discovery/source-availability rules and conditional acceptance categories only. Do not invent identity-transfer, signing-message, key-lifecycle, rotation, or unsigned-legacy interfaces.

**Trust/source/retention decisions:** Target content is untrusted data. Resolution is read-only and exact-SHA; execution uses disposable detached checkouts. Target execution has no provider secret or repository write permission. Model audit never executes target code and has no repository write permission. Publishing consumes validated canonical data and executes no target/PR code. Raw bundles are sealed before grading and request private 400-day Actions retention only when configuration supports it; validated manifests/reports persist on an append-oriented evidence branch with the hostile-host limitation stated.

**Clarify/analyze plan:** Run the Spec Kit clarify phase across the constitution, six specs, schemas, trust/source/retention documents, and target profile. Resolve only from approved dispositions or selected-SHA evidence; otherwise record `MISSING EVIDENCE` or hard-stop when required. Then build a PRD -> constitution -> FR -> acceptance -> schema -> source availability -> implementation task -> sabotage traceability matrix. NEF-T001 is incomplete unless `docs/cross-artifact-analysis.md` reports zero unresolved critical inconsistencies.

**Verification:** Parse every JSON Schema with the Python standard library; assert draft, IDs, versions, closed-object semantics, required fields, digest formats, and state enums; search for unresolved placeholders, state collapse, target-ref-without-SHA usage, model-authoritative language, and invented future capability details; verify all required requirements map through acceptance and later tasks; run `git diff --check`; inspect the complete diff; verify both NEST checkouts are unchanged; confirm `CLAUDE.md` remains exact.

**Risks:** normative schema freeze; moving-target drift; untracked `.targets/`; unborn NEF SHA; unsupported 400-day retention; stale time-sensitive research; current hash-chain privileged re-chain honesty boundary; duplication across six specs. Mitigations are versioned schemas, exact-SHA partitioning, never staging `.targets/`, explicit unavailable provenance, primary-source research register entries, capability-conditioned protocols, and one canonical vocabulary owner.

**Hard-stop audit:** No current trigger. Stop if implementation would require a new dependency/service, a change to a frozen threshold/baseline/protocol/ontology/advisory policy, real data/traffic/production keys, a second target system, hosted evaluation SaaS, external signing/anchoring, NEST modification, automatic remediation/promotion, a new provider/source transfer, billing/secrets, or a scope expansion beyond NEF-T001.

**Scope expansion:** none. No product implementation in NEF-T001.

## 2026-07-11 - NEF-T001 implementation and local verification

**Task / milestone:** NEF-T001, v1 goal specification foundation.

**Branch:** `docs/NEF-T001-specifications` (renamed from the unpushed bootstrap branch to Matthias's checkpoint convention). `origin` is exactly `https://github.com/maca-ai/nest-evaluation-framework.git`.

**Files changed:** the seven approved bootstrap package files form the initial repository baseline; NEF-T001 adds the constitution, specs 001-006, `specs/HANDOFF.md`, clarification record, eight normative JSON Schemas, research register, trust model, source-availability matrix, retention contract, public-interface contract, initial target profile, and cross-artifact analysis. `TASKS.md` and this append-only log were updated. No source, test, workflow, dependency, secret, provider, billing, or NEST file was added or changed.

**Target evidence:** NEST `main` was re-resolved read-only at goal start and remained `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`. The disposable detached checkout and Matthias's optional original local checkout remained clean. Selected target constitution = 1.3.0; protocol digest = `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`; environment fingerprint digest = `f49bc5597f657fbca2f7fe19e7c9586658036a6051cf940b4abff81caa254f3f`. T-014 and T-015 are available; T-016 and Ed25519 remain reasoned `skipped/unavailable` cases. The earlier orientation manifest is a pre-schema bootstrap journal record; the normative schemas now define version 1.0.0 serialized manifests, including `nef_sha` with an explicit unavailable-bootstrap alternative.

**Decisions:**

- Constitution 1.0.0 fixes exact-SHA read-only targeting, evidence-before-grading, six non-collapsible states, one campaign seam, capability conditioning, advisory findings, workflow separation, retention honesty, and budget honesty.
- Specs allocate shared contracts/evidence/orchestration to 001, target integrity to 002, mutation to 003, property/fuzz to 004, performance to 005, and model audit/quality checkpoint to 006.
- Normative schemas are JSON Schema draft 2020-12, version 1.0.0, closed at the top level, with UTC timestamps, lowercase digests, Decimal-as-string, and no JSON-number floats in hashed/threshold data.
- Spec Kit clarify recorded five explicit non-blocking `MISSING EVIDENCE` items and no unresolved critical clarification.
- Spec Kit analyze found and resolved A-001 through A-017, including missing pass evidence, ambiguous state mappings, manifest/digest mismatch, stale field naming, Decimal `oneOf` overlap, path/credential constraints, and future-capability overclaim risk.
- Cross-artifact result: zero unresolved critical inconsistencies.

**Exact verification commands and results:**

- `find specs/001-framework-contracts/contracts -name '*.json' -exec python3 -m json.tool {} /dev/null \;` - PASS, eight JSON documents parse.
- `python3 -c 'import json,pathlib; files=sorted(pathlib.Path("specs/001-framework-contracts/contracts").glob("*.json")); assert len(files)==8; docs=[json.loads(p.read_text()) for p in files]; assert all(d.get("$schema")=="https://json-schema.org/draft/2020-12/schema" for d in docs); assert all(d.get("additionalProperties") is False for d in docs); print("schema-structure: PASS")'` - PASS.
- `python3 -c 'import pathlib,re; specs=sorted(pathlib.Path("specs").glob("[0-9][0-9][0-9]-*/spec.md")); assert len(specs)==6; assert all(re.search(r"NEF-[0-9]{3}-FR-[0-9]{3}", p.read_text()) for p in specs); print("spec-structure: PASS")'` - PASS.
- `rg -n '\[NEEDS CLARIFICATION\]|TODO|TBD' specs docs` - PASS by no matches.
- `git grep --cached -n -E 'ghp_|github_pat_|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY'` - PASS by no matches.
- `git diff --cached --check` - PASS after removing Markdown hard-break trailing spaces found on the first run.
- `cmp -s CLAUDE.md <(printf '@AGENTS.md\n')` - PASS.
- `git -C .targets/nest/de8c0772dcb1890bfbf7c2c449a4252f63e0807a rev-parse HEAD` - PASS, exact selected SHA.
- `git -C .targets/nest/de8c0772dcb1890bfbf7c2c449a4252f63e0807a status --porcelain` - PASS by empty output.
- `git -C /Users/mc/Claude/Projects/NEST/nest-repo status --porcelain` - PASS by empty output.
- `git diff --cached --name-only | rg '^\.targets/'` - PASS by no matches; disposable target is not staged.
- `git remote -v` - PASS, fetch/push URLs exactly match the approved NEF repository.
- Required lint/type/test/security toolchain: not present by design before NEF-T002. T001 ran schema/spec structural checks and a staged secret-pattern scan; no product code exists to lint or typecheck.

**Diff review:** Complete staged baseline/task diff reviewed in groups: control package, task/session records, constitution/clarification/handoff, supporting documents, all eight schemas, and specs 001-006. Scope is limited to the 31 intended files; `.targets/` is the only unstaged path. No sensitive or unrelated change remains.

**Risks / known limitations:**

- The repository is unborn until this checkpoint commit; the orientation snapshot honestly records unavailable NEF SHA.
- `.targets/` remains untracked until NEF-T002 creates `.gitignore`; it must never be staged.
- Semantic metaschema validation library is not installed and was not added; T003 must prove generated-schema conformance. T001 performed JSON syntax and contract-structure assertions.
- GitHub artifact retention support remains unverified until NEF-T005.
- T-016/Ed25519 interfaces remain missing evidence and were not invented.
- Read-only `git ls-remote origin` returned no refs. The task branch can be pushed, but a draft PR targeting `main` cannot exist if the remote still has no base branch.

**Exact next action:** create the Conventional Commit checkpoint, push `docs/NEF-T001-specifications`, verify remote SHA equality, then attempt a draft PR to `main`. If GitHub refuses because `main` does not exist, stop and ask Matthias to establish/authorize the base branch; do not push directly to `main` or invent another base.

### Remote checkpoint outcome

- Local checkpoint commit: `aebd2b151dfb1252dd4c952d74dc8256b1975c5d` (`docs(specs): NEF-T001 define executable contracts`).
- Push: PASS; `docs/NEF-T001-specifications` created on `origin` and configured as the upstream branch.
- Remote SHA verification: PASS; `refs/heads/docs/NEF-T001-specifications` exactly matched `aebd2b151dfb1252dd4c952d74dc8256b1975c5d`.
- Draft PR command: `gh pr create --repo maca-ai/nest-evaluation-framework --base main --head docs/NEF-T001-specifications --draft --title "NEF-T001: define constitution and executable specifications" ...`.
- Draft PR result: FAIL. Exact GitHub error: `pull request create failed: GraphQL: Head sha can't be blank, Base sha can't be blank, No commits between main and docs/NEF-T001-specifications, Base ref must be a branch (createPullRequest)`.
- Cause: the approved GitHub repository was empty before this checkpoint and has no `main` ref/default branch. The pushed task branch is the only remote ref.
- CI/review: not started because no pull request exists; NEF-T002 has not yet created the CI scaffold.
- Task status: NEF-T001 remains In progress despite complete local acceptance because Matthias requires a draft PR at the task checkpoint.
- Smallest next action: Matthias creates or explicitly authorizes creation of a legitimate `main` base branch, then directs how the already-pushed root task commit should be related to that base without force-push, history rewrite, or a direct task commit to `main`. After that external decision, update/open the draft PR and wait for CI/review. Do not start NEF-T002 meanwhile.
