# PRD - nest-evaluation-framework (NEF)

## Problem and goal

NEST converts physical observations into governed, attested business objects. Per-PR CI protects individual diffs, but it does not continuously prove that the current whole-repository test suite kills realistic injected defects, hostile inputs cannot break governed surfaces, performance has not regressed relative to an approved reference, or independent review cannot find evidence-backed defects.

NEF's goal is an unattended daily evaluation window that selects one exact NEST revision, executes bounded adversarial and deterministic campaigns, distinguishes product failure from harness/evidence failure, preserves replayable evidence, and publishes advisory findings. A best-effort watchdog reports a missing daily result. Claim-corpus falsification against a running NEST product remains later work until NEST exposes the required runnable targets.

NEST is a versioned external target. A run evaluates an immutable commit SHA. Scored gate evidence defaults to the highest numeric milestone tag (`m0`, `m1`, ...), recording both the tag ref and peeled commit. Pre-tag work may run only as an explicitly acknowledged pinned-SHA provisional campaign labelled non-gate evidence and non-reproducible baseline. Branches, `HEAD`, and other moving refs are never recorded campaign selectors, and failed gate selection never silently falls back to provisional mode.

## Target users

- Matthias: reads reports, triages candidates, and records dispositions.
- The NEST builder: receives dated dispositions derived from confirmed findings.
- Advisor/reviewer instances: perform independent adversarial triage.
- Later: auditors, pilot customers, and funders who need reproducible evaluation evidence.

## Evaluation vocabulary

- **Run**: one evaluation of one NEST SHA under one protocol digest.
- **Campaign**: one configured evaluation class within explicit time, cost, and resource budgets.
- **Trial**: one attempt within a campaign; repeated trials remain distinct.
- **Case**: the smallest independently graded input, scenario, or mutant.
- **Finding**: a stable, deduplicated claim linked to evidence; it is not confirmed before triage.
- **Evidence bundle**: content-addressed raw inputs, outputs, logs, environment metadata, and digests sealed before grading.
- **Report**: a deterministic projection rebuilt only from validated manifests.
- **Disposition**: a dated human decision: `confirmed`, `rejected`, `needs-more-evidence`, `accepted-risk`, or `fixed`.
- **TargetSnapshotManifest**: provenance for the selected NEST source and environment.
- **TargetCapabilityManifest**: detected capabilities, integrity protocol, required campaigns, and explicit unavailable cases for that SHA.

## Core features

1. **Daily orchestration**: GitHub Actions schedule away from peak boundaries plus manual dispatch; acquire an exact target SHA; run bounded jobs; publish one canonical attempt; report a missing terminal manifest after 26 hours through a best-effort watchdog.
2. **Shared verification engine and evidence layer**: all campaigns use one versioned request/result interface, state semantics, sealing rules, and sabotage-based conformance suite.
3. **Deterministic target-integrity campaign**: verify the current canonical global hash chain and, only when present in the selected target, the ratified Ed25519 per-record signing protocol.
4. **Weapon A - mutation**: mutate an explicit inclusion manifest in disposable worktrees; shard within job limits; separately report killed, survived, timeout, invalid, and untested mutants.
5. **Weapon B - property/fuzz**: bounded Hypothesis property and stateful campaigns against declared available surfaces; retain minimized examples, reproduction data, versions, target SHA, and environment fingerprint.
6. **Weapon C - performance**: alternating paired trials of an approved reference SHA and target SHA on the same runner; store raw series, uncertainty policy, absolute floors, environment fingerprint, and protocol digest.
7. **Weapon D - adversarial model audit**: submit a size-bounded, secret-scanned source manifest as untrusted data without executing it; pin provider/model/request/prompt/input/schema/SDK/usage/response metadata; emit `supported` or `suspected` candidates only.
8. **Findings ledger**: stable fingerprints make GitHub Issue publication idempotent; recurrence updates an existing issue with a new run/evidence reference.
9. **Evidence retention**: retain content-addressed raw bundles as private Actions artifacts for 400 days when repository configuration supports it; persist validated manifests and deterministic reports on an append-oriented evidence branch. State the hostile-host limitation honestly.
10. **Later milestones**: claim corpus with source-digest drift detection; disposable/recorded NEST adapters and replay verification; scorecards rebuilt solely from validated manifests.

## Target-integrity requirements

### Immutable target pinning

Every campaign uses one of two immutable target modes. `gate-evidence` selects an `mN` milestone tag, defaulting to the highest numeric milestone, and records the tag-ref SHA plus the peeled commit SHA. Peeling an annotated tag dereferences its tag object; peeling a lightweight tag is the identity operation. `provisional` requires a specific acknowledged commit SHA and is always non-gate evidence with a non-reproducible-baseline label. The commit remains replayable; the label means it is not an accepted milestone baseline.

Prior validated snapshots are the immutable binding history. If a previously observed gate tag resolves to a different tag ref or peeled commit, NEF retains the new snapshot as violation evidence, refuses the campaign, and emits a deterministic candidate finding. Deleting prior history can evade this comparison; append-only/hash-chained snapshot history is the named later hardening seam.

### Current hash-chain protocol

Verify canonical record hashing, predecessor linkage, genesis, gap-free sequence, committed source identity, append-only behavior, reserved record-type handling, whole-chain verification, and head-anchor export. Historical VPS measurements are context only, not portable thresholds.

### T-016 namespaced identity capability

When exposed by the selected SHA:

- identical asset tags across deployments or sources never merge;
- sensor replacement preserves both old and new provenance;
- identity transfer is explicit and append-only;
- missing predecessors, cycles, conflicts, and cross-SPV collisions are refused according to NEST's ratified interface;
- dedup remains scoped to full namespaced source identity.

### Announced Ed25519 signing capability

Do not invent the signing message, key lifecycle, or legacy migration rule. Discover them from the selected SHA's ratified constitution, specification, design record, source, and executable fixtures. Once available, cover:

- a valid signed record;
- payload, record hash, predecessor, sequence, signature, algorithm, and key-ID tampering;
- wrong, unknown, retired, malformed, or missing public keys;
- missing, duplicate, malformed, and wrong-length signatures;
- insertion, deletion, reorder, replay, and backdated privileged append;
- a hash-valid re-chain without the private key failing signature verification;
- historical verification with the public key valid for the recorded epoch;
- key-compromise and administrator/history-rewrite honesty boundaries;
- unsigned legacy behavior exactly as NEST ratifies it.

Design checks use the eventual NEST implementation plus [RFC 8032](https://www.rfc-editor.org/info/rfc8032/), [NIST FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final), and the official [`cryptography` Ed25519 interface](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/). NEF never handles production private keys.

## Explicit non-goals

- No result gates a NEST merge in v1.
- No writes to NEST, NEST CI integration, or NEST dashboard changes.
- No real customer data, production shadow traffic, or secrets in evidence/model inputs.
- No production signing, key custody, or external evidence anchoring in v1.
- No plugin platform, arbitrary adapter registry, second system under evaluation, server, database, or auth backend.
- No managed evaluation SaaS dependency.
- No automatic issue closure, remediation, finding promotion, baseline promotion, or threshold change.
- No reinterpretation of NEST canon. NEST constitution/specifications and spec 004 metric dictionary remain authoritative for NEST behavior.
- No claim that GitHub retention is permanent or provider budget alerts enforce a spending ceiling.

## Success criteria

- Every scheduled date has one canonical run identity per target SHA and protocol digest; reruns are numbered attempts. A missing terminal manifest within 26 hours becomes a visible harness incident.
- Each job declares a timeout below platform limits. Timeout, cancellation, missing artifact, malformed output, and publication failure are explicit non-pass states.
- Every campaign has a sabotage proof demonstrating that it can fail.
- The target-integrity campaign catches tamper/re-chain fixtures appropriate to the capability manifest; unavailable future capabilities are visible skips.
- Mutation results publish the complete denominator and evidence for each survivor.
- Every fuzz failure replays from the retained minimized example in the pinned environment; failed replay is `inconclusive`.
- Performance reports retain raw paired series and a predeclared decision rule; noisy or insufficient samples are `inconclusive`.
- Results and trends are partitioned by target SHA, environment fingerprint, and integrity-protocol digest. Hash-only and signed-chain results are never compared as one protocol.
- Fourteen days after the first successful model-audit run, compare `supported` candidates with human dispositions. Under 50% confirmed defaults the model audit to weekly and reallocates allowance to fuzzing unless Matthias records another decision.
- Product failure, harness error, insufficient evidence, invalid case, and deliberate skip remain distinct; missing evidence never passes.
- Operating spend targets EUR 100-300/month. GitHub uses stop-usage controls where available; provider projects use alerts; NEF reserves a conservative application allowance before model calls and skips the model campaign when pricing evidence or allowance is insufficient.
- Target execution holds no provider secret/write token; publishing executes no target code; third-party actions are pinned by full commit SHA.
- A fresh agent can identify the project, target-access rule, current task, and next action from the seven-file package.
