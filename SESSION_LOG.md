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

## 2026-07-11 - NEF-T001 authorized repository-genesis disposition

**Disposition:** Matthias explicitly ruled that NEF-T001 is the repository genesis. Root commit `aebd2b151dfb1252dd4c952d74dc8256b1975c5d` necessarily created the seven-file control scaffold and the T001 specification artifacts together because no earlier baseline exists. A synthetic scaffold commit or replacement branch would manufacture a review diff and is prohibited.

**Genesis exception:** Matthias authorized one additive direct creation of `refs/heads/main` from the tip of `docs/NEF-T001-specifications`. This dated exception overrides the normal no-direct-push rule for that single genesis push only. It does not authorize a force-push, history rewrite, self-merge, credential handling, or any later direct push to `main`.

**Supersession:** This disposition supersedes the preceding `blocked / awaiting PR checkpoint` status. NEF-T001 is complete as the authorized bootstrap genesis. The lack of a T001 pull-request diff is intrinsic to the repository's creation, not a waiver for subsequent work.

**Mandatory discipline from NEF-T002 onward:** Every task branches from `main`, produces a real reviewable diff, passes proportionate local verification and required GitHub CI/spec-blind review, creates a recoverable pushed checkpoint and draft pull request targeting `main`, and waits at applicable approval/merge boundaries. No later task may rely on the genesis exception.

**Genesis checkpoint method:** Commit this disposition on `docs/NEF-T001-specifications`, push that exact branch tip additively to `refs/heads/main`, set the GitHub default branch to `main`, and verify the remote ref. If GitHub branch protection rejects creation, stop without workaround. The exact resulting main SHA and remote verification evidence will be appended from the first normal task branch because a Git commit cannot record its own SHA in its own contents.

**Target context:** NEST target SHA remains `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`; integrity-protocol digest remains `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`. The target capability manifest remains current: T-014 and T-015 available; T-016 and Ed25519 explicit `skipped/unavailable` cases.

**Exact next action:** verify and commit only `TASKS.md` and `SESSION_LOG.md` on `docs/NEF-T001-specifications`, push the task branch checkpoint, then create `main` at that same exact tip under the one-time authorization.

## 2026-07-12 - NEF-T002 goal-mode implementation plan

**Genesis closeout evidence:** Authorized additive genesis creation succeeded. `refs/heads/main` and `refs/heads/docs/NEF-T001-specifications` both resolve to `d3d22bd6690323a495d10b9b3812bf7457d286da`; GitHub reports `main` as the default branch. The task branch is retained as a recovery reference. The one-time exception is exhausted. NEF-T002 branches from verified `origin/main` as `feat/NEF-T002-reproducible-scaffold` and returns to mandatory draft-PR discipline.

**Task / milestone:** NEF-T002 - Reproducible scaffold and trusted CI; v1 foundation milestone. It is the top eligible Pending task and the only implementation task in progress.

**Target refresh before design:** At `2026-07-12T05:31:18Z`, read-only `git ls-remote https://github.com/maca-ai/nest.git refs/heads/main` resolved the configured moving ref to `1e989338e4f67342ecb5139a58aaaa64fb70b295`, not the prior T001 SHA. A new disposable detached checkout exists at `.targets/nest/1e989338e4f67342ecb5139a58aaaa64fb70b295`; it is clean, has tree `8b8c4b795d1024b41e50ac5175af0163a869f13c`, commit time `2026-07-11T16:25:24+02:00`, and subject `feat(core): T-016 namespaced identity + sensor-replacement event + rdo-created emission (#19)`. The optional original local checkout is also clean at that exact SHA. No NEST test or campaign ran and no NEST file was written.

**Target snapshot:** repository `https://github.com/maca-ai/nest.git`; requested ref `main`; exact SHA `1e989338e4f67342ecb5139a58aaaa64fb70b295`; detached/clean; NEF SHA `d3d22bd6690323a495d10b9b3812bf7457d286da`; target lock digest `5b6f7af0cd9f72e75e30a384ba0b95b809544032e91b283513784a6b29494186`; constitution 1.3.0 digest `6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a`; expanded integrity-protocol digest `b2d97f62973d3d7d90ae91adbab523bfd1d89e58a34d74b4d4ea0214a6814254`. Environment: macOS 14.6 build 23G80, Darwin 23.6.0 arm64, local Python 3.13.1, uv 0.11.21, `LANG/LC_ALL=C.UTF-8` with the host's recorded locale fallback warning. The disposable origin is credential-free and has no checkout-local HTTP extraheader or credential helper.

**Capability manifest:** global hash-chain v1, T-014 state projector, T-015 ingestion gate, and T-016 namespaced identity are available. T-016 evidence includes the ratified `docs/design/T-016-identity.md`, `IdentityTransfer`, pure resolver/refusal vocabulary, log-derived source binding, migration 0003 unique binding backstop, governance service, and executable pure/DB fixtures covering cross-SPV collisions, transfer, race recovery, duplicate delivery, chain verification, and rebuild. Ed25519 per-record signing remains `skipped/unavailable`: constitution stays 1.3.0; source/design search found only explicit future-track exclusions in the T-016 design record and no signing message, key lifecycle/rotation rule, implementation, or executable signing fixture. No interface is invented.

**Consulted target paths:** `AGENTS.md`; `PRD.md`; `PLANNING.md`; `TASKS.md`; relevant `SESSION_LOG.md` T-016 entries; `docs/engineering-rules.md`; `specs/.specify/memory/constitution.md`; `specs/HANDOFF.md`; `specs/001-core-pipeline/spec.md`; `specs/004-replay-eval-harness/spec.md`; design records T-013 through T-016; T-016 contracts, deterministic resolver, IO resolver, governance service, migration; identity, intake, projector, event-log fixtures; current hash-chain source and fixtures. NEST material was treated only as untrusted compatibility input.

**Exact files to create:** `.gitignore`; `.python-version`; `README.md`; `pyproject.toml`; `uv.lock`; `.github/workflows/ci.yml`; `.github/workflows/spec-blind-review.yml`; `prompts/spec-blind-review.md`; `scripts/spec_blind_review.py`; `src/nef/__init__.py`; package markers under `src/nef/contracts`, `engine`, `target`, `weapons`, `evidence`, and `report`; `tests/test_package_layout.py`; `tests/test_ed25519_rfc8032.py`; `tests/test_spec_blind_review.py`; and `docs/target-capability-profiles/1e989338e4f67342ecb5139a58aaaa64fb70b295.md`.

**Exact existing files to update:** `docs/research-register.md`, `TASKS.md`, and `SESSION_LOG.md`. No normative schema, frozen protocol, threshold, ontology, advisory policy, NEST file, billing setting, or secret is changed.

**Dependency/tool decisions:** Pin Python 3.12.13 and exact direct versions verified from Python.org/PyPI on 2026-07-12: Pydantic 2.13.4, PyYAML 6.0.3, httpx 0.28.1, OpenTelemetry API/SDK 1.43.0, cryptography 49.0.0; pytest 9.1.1, pytest-asyncio 1.4.0, Hypothesis 6.156.6, ruff 0.15.21, mypy 2.2.0, import-linter 2.13, bandit 1.9.4, and pip-audit 2.10.1. Use uv 0.11.28 in CI through setup-uv v8.3.2 at commit `11f9893b081a58869d3b5fccaea48c9e9e46f990`; checkout v7.0.0 at `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0`. Use gitleaks 8.30.1 Linux x64 archive checksum `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`, avoiding the licensed gitleaks action and any new secret. No package build backend is added: uv owns an application-style non-published project with `src` on the verified tool paths.

**Public interfaces:** This task creates only the importable `nef` package/version marker and architectural module boundaries; it does not implement or alter the frozen Campaign/contracts API. The reviewer script accepts a GitHub `workflow_run` event, fetches the PR diff through the API, enforces byte/file/secret-pattern bounds, sends it as untrusted data to Anthropic, validates a closed JSON candidate-review shape, and emits an advisory artifact. Its model is canonical pinned snapshot `claude-fable-5`; sampling parameters are omitted because Fable rejects non-default sampling; maximum output and schema are fixed. No model verdict gates a merge.

**Workflow trust design:** Unprivileged `pull_request`/push CI gets read-only contents and executes PR code with no provider secret or write token. The spec-blind workflow uses `workflow_run` after successful CI, checks out only trusted default-branch code at the event's repository default SHA, never checks out PR code, fetches the bounded diff as data, has read-only repository permission, and exposes only `ANTHROPIC_API_KEY`. It uploads/prints advisory evidence without commenting or mutating GitHub. The T002 PR can run the new unprivileged CI and locally test the privileged workflow implementation, but GitHub cannot run a newly introduced `workflow_run` definition until it exists on the default branch; that bootstrap limitation remains explicit and is not worked around with privileged head code.

**Tests and cross-artifact analysis:** Test importability and module inventory; verify pyproject pins and workflow action SHAs; apply RFC 8032 Ed25519 test vector 1 using synthetic fixture bytes and prove message/signature/public-key tampering fails independently; unit-test diff bounds, secret refusal, response schema/stop-state validation, and prompt/data separation without network. Cross-check task, plan, README commands, lock, CI commands, module layout, trust model, research register, target profile, and T001 frozen specs. Missing provider credentials skip external reviewer execution rather than fabricate success.

**Verification commands:** `uv lock --check`; `uv sync --locked --all-groups`; `uv run --locked ruff format --check .`; `uv run --locked ruff check .`; `uv run --locked mypy --strict src tests scripts`; `uv run --locked pytest`; `uv run --locked lint-imports`; `uv run --locked bandit -q -r src scripts`; `uv export --locked --no-dev --no-emit-project --format requirements-txt` followed by `uv run --locked pip-audit -r <export>`; local gitleaks 8.30.1 scan if the verified binary is available; JSON/YAML parse and action-pin assertions; `git diff --check`; CLAUDE invariant; target checkout/original checkout clean checks; staged and complete branch diff review.

**Risks:** moving-target capability drift; first privileged-review workflow bootstrap; action/tool supply chain; Python 3.12 source-only upstream lifecycle; model retention/cost and prompt injection; accidentally staging `.targets/`; security scanner false negatives; empty skeleton making architectural checks vacuous. Mitigations: immutable target profile per SHA, explicit bootstrap limitation, exact action/tool/package pins and lock, bounded/advisory trusted-base review, `.gitignore` first, sabotage tests for reviewer refusal, import-linter boundary contract, and no target/provider execution in scaffold tests.

**Hard-stop audit:** No current hard-stop. All dependencies and providers are already allowed by `PLANNING.md`; no billing, secret, remote, NEST, schema, protocol, threshold, ontology, or advisory-policy mutation is planned. Stop if a required package or action cannot be verified, a security check repeats the same failure twice, GitHub requires unsafe privileged execution, provider configuration/secret creation is needed, or acceptance would require changing a frozen artifact.

**Scope expansion:** Only the required target-refresh profile and genesis remote evidence accompany NEF-T002; both are mandated by the goal and do not alter target behavior. No NEF-T003 contract implementation begins.

## 2026-07-12 - approved immutable target-pinning amendment

**Supersession and authority:** Matthias approved this dated amendment after the preceding NEF-T002 plan had begun but before any checkpoint. It supersedes that plan's moving-`main` target-selection assumption and explicitly authorizes the breaking target-contract, constitution, and development-dependency changes below. Historical observations remain append-only. The earlier `de8c0772dcb1890bfbf7c2c449a4252f63e0807a` and `1e989338e4f67342ecb5139a58aaaa64fb70b295` records are retained and reclassified as provisional/non-gate evidence rather than erased or rewritten.

**Approved target-selection law:** Recorded campaigns never select a mutable ref. Default scored evidence uses the highest numeric NEST milestone gate tag matching `mN`; numeric ordering makes `m10` later than `m9`. The selected tag is resolved at pin time to both its tag-ref SHA and its peeled commit SHA. Peeling an annotated tag dereferences the tag object; peeling a lightweight tag is the identity operation because its tag-ref SHA is already a commit. Explicit pre-gate evaluation uses only an acknowledged exact commit SHA and is labelled `provisional`, `non-gate-evidence`, and `non-reproducible-baseline`. It remains byte-replayable by SHA; the baseline label means it cannot support milestone scoring. Missing gate tags never trigger a provisional fallback.

**Pin-time remote evidence:** At `2026-07-12T07:31:38Z`, read-only tag enumeration for `https://github.com/maca-ai/nest.git` returned only annotated gate tag `m0`: tag-ref SHA `8362f666336c429812fbf32aabc8eaaf1d9ac47a`, peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`. `m1` is absent. A disposable clone was checked out detached and clean at `.targets/nest/cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`; tree `77ccd2fc1a41dd365a3b3b98508bb0534b56c95f`; commit time `2026-07-09T08:17:50+02:00`; subject `T-004: M0 gate passed — sign-off recorded, M0 complete (#6)`. Its origin URL contains no userinfo. No target test or campaign ran and no target file was written. Matthias's optional original local NEST checkout was clean before inspection at independent SHA `83d5bbddc5368aea921b368096b611c509a51403` and remains planning context only.

### TargetDescriptor 2.0.0 - gate default

```yaml
schema_version: 2.0.0
repository_url: https://github.com/maca-ai/nest.git
target_mode: gate-evidence
selector:
  kind: gate-tag
  gate_tag: m0
  tag_ref_sha: 8362f666336c429812fbf32aabc8eaaf1d9ac47a
resolved_sha: cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12
observed_at: 2026-07-12T07:31:38Z
source_kind: remote
```

### TargetSnapshotManifest 2.0.0 - m0

```yaml
schema_version: 2.0.0
repository_url: https://github.com/maca-ai/nest.git
target_mode: gate-evidence
selector:
  kind: gate-tag
  gate_tag: m0
  tag_ref_sha: 8362f666336c429812fbf32aabc8eaaf1d9ac47a
resolved_sha: cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12
evidence_class: gate-evidence
baseline_reproducibility: reproducible-baseline
tag_binding:
  state: first-seen
  previous_snapshot_manifest_digest: null
  previous_tag_ref_sha: null
  previous_resolved_sha: null
dirty: false
nef_sha: d3d22bd6690323a495d10b9b3812bf7457d286da
lock_digest: 9f5e25f611865b3e37951b5975c27af4ed1229a1610f7bff00418aa56059e853
constitution_version: 1.3.0
constitution_digest: 6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a
protocol_digest: e875521b803d5418c52343a536d2dcee98e506c87342db1979ffc266d7fde714
relevant_source_digests:
  docs/DECISIONS-2026-07-06-REDTEAM.md: 55e61cb1b5a87e4ccd151828cb7bd2416b3f14009470402e3364b31bb6a92a91
  specs/.specify/memory/constitution.md: 6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a
  specs/001-core-pipeline/spec.md: 1a095743c37a0c3de7a3db36e9a0e8137aac8c92e7bb73096d0a5421a9d501f1
environment_fingerprint:
  digest: edd95b9acf193017415adb447894aa5b2dd13057729633531d1e85522631ab40
  runner: local-codex
  operating_system: macOS 14.6 build 23G80
  architecture: arm64
  locale: C.UTF-8 (host fallback C)
  timezone: Europe/Vienna
  tool_versions:
    python: 3.13.1
    uv: 0.11.21
consulted_paths:
  - AGENTS.md
  - PRD.md
  - PLANNING.md
  - TASKS.md
  - SESSION_LOG.md
  - specs/.specify/memory/constitution.md
  - specs/HANDOFF.md
  - specs/001-core-pipeline/spec.md
  - specs/004-replay-eval-harness/spec.md
  - docs/DECISIONS-2026-07-06-BUILD-AUDIT.md
  - docs/DECISIONS-2026-07-06-REDTEAM.md
  - packages/nest-core/README.md
  - packages/nest-core/pyproject.toml
  - packages/nest-core/src/nest_core/__init__.py
  - packages/nest-core/tests/test_smoke.py
  - pyproject.toml
  - uv.lock
observed_at: 2026-07-12T07:31:38Z
```

**Protocol inputs and digests:** `specs/.specify/memory/constitution.md` = `6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a`; `specs/001-core-pipeline/spec.md` = `1a095743c37a0c3de7a3db36e9a0e8137aac8c92e7bb73096d0a5421a9d501f1`; `docs/DECISIONS-2026-07-06-REDTEAM.md` = `55e61cb1b5a87e4ccd151828cb7bd2416b3f14009470402e3364b31bb6a92a91`. The protocol digest is SHA-256 of their lexicographically sorted `sha256  path` lines. Environment input: local Codex runner, macOS 14.6 build 23G80, arm64, `C.UTF-8` with host fallback `C`, Europe/Vienna, Python 3.13.1, uv 0.11.21.

### TargetCapabilityManifest - m0

```yaml
schema_version: 1.0.0
target_sha: cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12
protocol_digest: e875521b803d5418c52343a536d2dcee98e506c87342db1979ffc266d7fde714
capabilities:
  - capability_id: target-binding
    state: available
    evidence:
      - annotated m0 tag-ref 8362f666336c429812fbf32aabc8eaaf1d9ac47a peeled to cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12
    reason: null
  - capability_id: global-hash-chain-v1
    state: unavailable
    evidence:
      - packages/nest-core contains only package metadata, a package marker, and a smoke test
    reason: no event-log implementation, migration, verifier, or executable chain fixture at m0
  - capability_id: t-014-state-projector
    state: unavailable
    evidence:
      - capability search found no projector implementation or executable fixture at m0
    reason: implementation and executable fixture are absent
  - capability_id: t-015-ingestion-gate
    state: unavailable
    evidence:
      - capability search found no ingestion-gate implementation or executable fixture at m0
    reason: implementation and executable fixture are absent
  - capability_id: t-016-namespaced-identity
    state: unavailable
    evidence:
      - capability search found no namespaced-identity implementation or executable fixture at m0
    reason: implementation and executable fixture are absent
  - capability_id: ed25519-per-record-signing
    state: unavailable
    evidence:
      - constitution 1.3.0 and searched source expose no ratified signing protocol or fixture
    reason: ratified message, key lifecycle, implementation, and executable fixture are absent
required_campaigns:
  - target-integrity/target-binding
unavailable_campaigns_with_reasons:
  - campaign_id: target-integrity/global-hash-chain-v1
    state: skipped
    reason: global chain behavior is specified but not executable at m0
    missing_evidence:
      - event-log implementation
      - migration
      - verifier
      - executable chain fixture
  - campaign_id: target-integrity/t-014-state-projector
    state: skipped
    reason: T-014 is not implemented at m0
    missing_evidence:
      - projector implementation
      - executable projector fixture
  - campaign_id: target-integrity/t-015-ingestion-gate
    state: skipped
    reason: T-015 is not implemented at m0
    missing_evidence:
      - ingestion-gate implementation
      - executable ingestion-gate fixture
  - campaign_id: target-integrity/t-016-namespaced-identity
    state: skipped
    reason: T-016 is not implemented at m0
    missing_evidence:
      - ratified implementation
      - executable identity fixture
  - campaign_id: target-integrity/ed25519-per-record-signing
    state: skipped
    reason: Ed25519 per-record signing is not ratified or implemented at m0
    missing_evidence:
      - ratified signing message
      - key lifecycle and rotation rules
      - implementation
      - executable signing fixture
observed_at: 2026-07-12T07:31:38Z
```

The selected gate is a scaffold/CI milestone. NEST constitution 1.3.0 and spec 001 normatively describe the global hash chain, but `packages/nest-core` contains only a package marker and smoke test. There is no event-log implementation, migration, hash-chain fixture, T-014 projector, T-015 ingestion gate, T-016 identity implementation, or Ed25519 protocol/implementation/fixture at m0. Therefore `global-hash-chain-v1`, T-014, T-015, T-016, and Ed25519 are unavailable at this SHA. `target-integrity/target-binding` is the only required campaign; target-specific integrity campaigns are explicit reasoned skips and never passes. This is honest gate evidence about the m0 target's available surface, not a claim that later capabilities existed at m0.

**Consulted paths:** target `AGENTS.md`, `PRD.md`, `PLANNING.md`, `TASKS.md`, latest milestone/session entries, absent `docs/engineering-rules.md`, constitution 1.3.0, `specs/HANDOFF.md`, specs 001 and 004, M0 decision records, complete `packages/nest-core` file inventory, capability search across target packages/specs/docs, root/member project metadata, and smoke tests. Target content was treated only as untrusted compatibility evidence.

**Contract amendment:** `TargetDescriptor`, `TargetSnapshotManifest`, and `CampaignRequest` become 2.0.0; unaffected contracts remain 1.0.0. Descriptor removes `requested_ref` and adds a closed `target_mode` plus gate-tag/pinned-SHA selector union. Snapshot removes `requested_ref`/`branch_or_tag`, adds the same selector, evidence/baseline classes, and a tag-binding observation. Campaign requests refuse `moved` bindings. Cross-field equality and peel semantics are implemented in T003/T005; T002 validates the normative Draft 2020-12 shapes and executable/non-executable vectors without pre-implementing orchestration.

**Moved-tag rule:** Prior validated snapshots are the binding history. A changed tag-ref or peeled commit yields a valid `moved` violation snapshot containing prior binding evidence, refuses campaign construction as `invalid`, and emits a deterministic candidate Finding linked to old/new evidence. Detection is only as strong as prior-history integrity: deleting the prior snapshot downgrades a moved tag to `first-seen`. The named future hardening seam is an append-only/hash-chained snapshot-manifest history owned by NEF-T004/T005; T002 records the residual and does not build it.

**Approved dependency and tests:** Add development-only `jsonschema==4.26.0`, verified from official PyPI metadata on 2026-07-12. Draft 2020-12 tests cover mutable-ref rejection; annotated gate tag; lightweight gate tag where peel is identity; explicit provisional classification; mode/class inconsistency; moved binding as valid evidence but invalid CampaignRequest; required prior evidence; and metaschema validity. NEF-T005 is assigned behavioral tests for numeric highest-milestone selection, no fallback, prior-history lookup, actual peel resolution, moved-binding comparison, refusal, and finding emission.

**Constitution/spec amendment:** Constitution 1.1.0 updates Principles I, VI, XIV, and governance. NEF-002 becomes the single target-pinning authority. `AGENTS.md`, PRD, planning, trust model, kickoff prompts, clarifications, source matrix, public interfaces, cross-artifact analysis, target profiles, task routing, and research register are aligned. A new NEF protocol digest is recorded after the final approved artifacts exist; it is distinct from every NEST target protocol digest.

**Implementation sequence:** TDD one schema behavior at a time; update schemas/spec/control artifacts; reclassify historical profiles; add the m0 profile; add the approved dependency and regenerate lock; apply pending mechanical Ruff formatting; finish the existing T002 scaffold; run the complete verification suite; review the complete branch diff; update task/session evidence; commit and push only the task branch; open a draft PR to `main`; wait for CI/review and the merge approval boundary. Genesis is exhausted.

**Hard-stop audit:** Matthias explicitly approved the frozen-schema, constitution, baseline-policy, and dependency changes. No NEST write, external tag mutation, secret/billing configuration, second target, hosted service, model gate, customer data, production key, automatic promotion, force-push, or direct-main action is authorized or planned.

## 2026-07-12 - NEF-T002 implementation checkpoint prepared

**Task / milestone:** NEF-T002 - Reproducible scaffold and trusted CI; v1 foundation milestone. Implementation and proportionate local verification are complete. The task remains open until the branch checkpoint is pushed, the draft PR exists, required GitHub CI/review evidence is assessed, and Matthias approves the merge boundary.

**Branch and repository:** `feat/NEF-T002-reproducible-scaffold`, based on verified `origin/main` at `d3d22bd6690323a495d10b9b3812bf7457d286da`. `origin` fetch/push is exactly `https://github.com/maca-ai/nest-evaluation-framework.git`. The branch is neither `main`/`master` nor detached. The worktree contains only the intended T002 scaffold, approved target-pinning amendment, target profiles, tests, and control/evidence updates; nothing is staged at this record point.

**Files changed:** Created `.gitignore`, `.python-version`, `README.md`, `pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`, `.github/workflows/spec-blind-review.yml`, `prompts/spec-blind-review.md`, `scripts/spec_blind_review.py`, the seven `src/nef` package markers, four test modules, and target profiles for `1e989338e4f67342ecb5139a58aaaa64fb70b295` and `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`. Updated `AGENTS.md`, `PRD.md`, `PLANNING.md`, `TASKS.md`, `build-kickoff-prompt.md`, constitution 1.1.0, specs 001/002 and clarifications, the TargetDescriptor/TargetSnapshotManifest/CampaignRequest 2.0.0 schemas, public interfaces, trust model, source matrix, cross-artifact analysis, research register, the historical `de8c077...` target profile, and this session log. `CLAUDE.md` remains byte-for-byte `@AGENTS.md` plus one final newline.

**Implemented decisions:** Python 3.12.13 and every direct dependency/tool are exactly locked. CI uses read-only permissions, full-SHA actions, format/lint/strict-type/test/architecture/security/dependency/secret checks, and no provider secret. The separate advisory reviewer runs only after successful same-repository PR CI from trusted `main` code, never checks out PR code, bounds and secret-scans the diff, treats it as untrusted JSON data, validates a closed candidate-only response, and has no write permission. The newly introduced `workflow_run` cannot execute for the T002 PR until its definition exists on the default branch; T002 therefore verifies its code and sabotage paths locally and does not work around the bootstrap limitation by executing secret-bearing PR-head code.

**Target-pinning amendment:** TargetDescriptor, TargetSnapshotManifest, and CampaignRequest are 2.0.0; unaffected contracts remain 1.0.0. Gate evidence defaults to the highest numeric `mN`, records tag-ref plus peeled commit, permits annotated and lightweight identity peeling, and never falls back. Provisional work requires an acknowledged exact SHA and is non-gate/non-reproducible-baseline. Prior validated snapshots supply binding history; moved bindings remain valid violation evidence, are refused as CampaignRequest input, and require a deterministic candidate Finding in T005. The deletion weakness and later append-only/hash-chained T004/T005 hardening seam remain explicit.

**Current NEST target evidence:** A final read-only `git ls-remote --tags https://github.com/maca-ai/nest.git` recheck returned only unchanged annotated `m0`: tag-ref `8362f666336c429812fbf32aabc8eaaf1d9ac47a`, peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`; `m1` remains absent. The disposable checkout remains detached and clean at the peeled commit. Current NEST target protocol digest is `e875521b803d5418c52343a536d2dcee98e506c87342db1979ffc266d7fde714`; current capability disposition is target-binding required/available and global-chain, T-014, T-015, T-016, and Ed25519 reasoned unavailable skips at m0.

The optional original NEST checkout was rechecked read-only and had independently drifted since orientation: it remains at `83d5bbddc5368aea921b368096b611c509a51403` on `feat/T-026-ed25519-signing`, is one commit behind its upstream, and now contains untracked `scripts/ci/build_status.py`. No NEF command wrote there, no test/campaign ran there, and it is excluded from target execution and checkpoint inputs. This drift is retained as evidence rather than described as clean or silently removed.

**NEF protocol digest:** `5cf8f5fc9d39b04bd3eb4513406ee175148610407d6a76491e20942c4a07406b`. Construction is SHA-256 over lexicographically sorted `sha256  path` lines for constitution 1.1.0, specs 001/002, all eight normative schemas, `docs/public-interfaces.md`, `docs/trust-model.md`, and `docs/source-availability-matrix.md`. Input digests are: constitution `ce11ee3bb3352b2ac972efd12d3fc8bbe1b6ea84e1e54bc66fd8fb65a6168d2a`; spec 001 `e908fdb12b04a838430c22b74fa2438d8ff6dee0e2ea3c97e3f874e2322c0238`; spec 002 `eaeac7613da3c452be6a414ed4fb035cbc379d50bf01f83bd577194af5d55869`; TargetDescriptor `9b913c8a779aa2aafa873f1418a707b52aee0d7607fd059cfb013f521e984d9d`; TargetSnapshotManifest `e289492ed157ad2442d6c008027bf7217f1326ec5334117a98f6473be20b3fdd`; TargetCapabilityManifest `39fce559908bb2e1cdee28ac30a449b69a9e488be89420f5b8a4f35ba6c07530`; CampaignRequest `d4d441290b0847c785d59f9f784448614eab5fdf7c134d161cdd933eddae4adb`; CampaignResult `ec5e2b173fd1ba576fea6edcd5b160d604c75c079c3bf3128d2059a4749d71eb`; EvidenceManifest `70fb0ec8b94986ef1c6debb3e4d54f8f4f2c6629acabdc25d1648d3dc26f57c6`; Finding `ce22240176472ecd5ac934aa5e00f66e1144fb400a92dd340ed430573bfcacaf`; Disposition `6b946c532ef9f551d3b44dd6959c18674cb5cffb2fde45faa97ac6c167bf423a`; public interfaces `aa14801415498d601dc4ca5552dda3ae227e2230f92ba5141f236972b3d57698`; trust model `5c340e0eefe761861eb8f84cad4c1a393078abb7ac4472789d5e18349933397b`; source matrix `b4751efed63e1125eea10485e3e322e3da78dd493ee57b38b26d4fc56d9d3c50`.

**Verification evidence:**

- `UV_CACHE_DIR=/tmp/nef-uv-cache uv sync --offline --locked --all-groups` - PASS, 67 packages resolved and 65 checked.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv lock --check` - PASS, 67 packages resolved with no drift.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked ruff format --check .` - PASS, 12 files already formatted after the approved mechanical Ruff pass.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked ruff check .` - PASS.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked mypy --strict src tests scripts` - PASS, 12 source files, zero issues.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked pytest` - PASS, 34 tests including 17 target-pinning schema tests, 9 reviewer tests, 5 RFC 8032 tests, and 3 layout/workflow tests.
- `UV_CACHE_DIR=/tmp/nef-uv-cache PYTHONPATH=src uv run --offline --locked lint-imports` - PASS, one architecture contract kept.
- `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked bandit -q -r src scripts` - PASS.
- `uv export --offline --locked --no-dev --no-emit-project --format requirements.txt --output-file /tmp/nef-requirements.txt` followed by `UV_CACHE_DIR=/tmp/nef-uv-cache uv run --offline --locked pip-audit --cache-dir /tmp/nef-pip-audit-cache --disable-pip --require-hashes --requirement /tmp/nef-requirements.txt` - PASS, no known vulnerabilities.
- Official gitleaks v8.30.1 Darwin arm64 archive checksum `b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5` matched the official release checksum; `/tmp/nef-gitleaks-v8.30.1/gitleaks dir --redact --no-banner .` - PASS, no leaks in the working tree. CI independently verifies the pinned Linux archive checksum before scanning Git history.
- `git diff --check` - PASS.
- `test "$(cat CLAUDE.md)" = '@AGENTS.md'` and final-byte newline check - PASS.
- `.DS_Store` repository search - PASS, absent; `.gitignore` contains `.DS_Store` and `.targets/`.
- Final remote tag check and disposable checkout status - PASS, unchanged binding and detached clean target.

**Known limitations and risks:** The T002 PR itself cannot trigger a workflow newly introduced only in its head; first live secret-bearing spec-blind execution is available only after trusted merge to `main`. The reviewer is advisory and provider/model failures remain non-success. Import-linter currently proves a deliberately sparse boundary graph. Moved-tag detection depends on retained prior snapshots until T004/T005 harden the history. The m0 gate cannot exercise later NEST product-integrity campaigns. The independently dirty original NEST checkout is not evaluation input.

**Exact next action:** Review the final unstaged and staged diffs, stage only the listed T002 files, create the required Conventional Commit checkpoint, push `feat/NEF-T002-reproducible-scaffold`, verify remote/local SHA equality, open a draft PR to `main`, and inspect GitHub CI/review status. Do not merge or begin NEF-T003 without the applicable approval.

**Append-only commit-message correction:** The implementation commit `5ba3b760ddb7ae4201556a6655b5109b85179431` was created with the intended Conventional Commit subject and What/Why/Verification headings, but shell interpolation expanded backtick-delimited verification commands into their output. The expansion reran locked checks (including a successful dependency audit); a bare `gitleaks` lookup failed because the verified binary is intentionally at `/tmp/nef-gitleaks-v8.30.1/gitleaks`. No source or history was changed by those command substitutions, no secret was printed, and the implementation commit itself succeeded. History will not be amended or rewritten. This journal update and a follow-up Conventional Commit preserve an append-only correction with literal exact commands. The local branch tip has not yet been pushed.

**Revised exact next action:** Commit this transparent metadata correction with literal verification commands, run the committed gitleaks history scan, push the two additive commits, verify remote/local SHA equality, and open the draft T002 PR to `main`.
