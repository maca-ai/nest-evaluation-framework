# Feature specification: Immutable target pinning and integrity

**Spec:** NEF-002
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001 contracts, NEF constitution

## Goal

Pin, acquire, fingerprint, and evaluate one immutable read-only NEST revision while distinguishing scored milestone evidence from provisional pre-gate evaluation and conditioning integrity cases on capabilities that are actually ratified and executable at that SHA.

## User story 1 - Pin an immutable target

As an evaluator, I know exactly which NEST revision was inspected, why it was selected, and whether it counts as milestone evidence.

### Acceptance scenarios

1. Given gate mode with no explicit tag, when tags are enumerated, then only `mN` names are eligible and the highest numeric milestone is selected (`m10` after `m9`).
2. Given an annotated gate tag, when pinned, then its tag-ref SHA and peeled commit SHA are recorded; given a lightweight gate tag, peeling is the identity and both SHAs are equal.
3. Given provisional mode, when pinned, then the selector is an explicitly acknowledged exact commit SHA and the snapshot is `non-gate-evidence` and `non-reproducible-baseline`.
4. Given `main`, `HEAD`, a branch, `latest`, or another mutable ref as the recorded selector, when validation runs, then the target is invalid by construction even if a SHA is also supplied.
5. Given no eligible gate tag, when default gate selection runs, then it refuses and never falls back to provisional mode.
6. Given the pinned SHA cannot be fetched, when acquisition runs, then it stops with missing evidence and never substitutes another revision.
7. Given a disposable checkout, when inspected, then it is detached, clean, credential-free, and located under `.targets/nest/<sha>/`.
8. Given Matthias's original local checkout, when optional planning inspection completes, then its before/after status is identical and no target test ran there.

## User story 2 - Detect moved gate tags

As an investigator, I receive an explicit integrity violation if a milestone tag changes after NEF first observes it.

### Acceptance scenarios

1. Given no prior validated snapshot for a gate tag, when pinned, then the binding state is `first-seen` and the tag-ref/peeled-commit pair becomes immutable history.
2. Given a prior snapshot with the same tag-ref and peeled commit, when pinned again, then the binding state is `unchanged` and the campaign may proceed.
3. Given either the tag-ref or peeled commit differs from prior history, when pinned, then a `moved` snapshot is retained as violation evidence, campaign construction is refused as `invalid`, and a deterministic candidate Finding links the old and new evidence.
4. Given prior binding history was deleted, when a moved tag is observed, then detection may downgrade to `first-seen`; the report states this residual rather than claiming stronger protection.

## User story 3 - Complete target provenance

As an investigator, I can reproduce why a capability was considered available for one target SHA.

### Acceptance scenarios

1. Given a selected SHA, when snapshot creation completes, then repository, target mode, immutable selector, resolved SHA, evidence/baseline class, tag binding when applicable, dirty state, NEF revision, lock/constitution/protocol/source digests, environment, consulted paths, and observation time are present.
2. Given an unborn NEF repository during bootstrap, when a snapshot is recorded, then `nef_sha` carries an explicit unavailable reason rather than a fabricated SHA.
3. Given a changed relevant source file at a future SHA, when the protocol digest is recomputed, then results partition from the previous protocol.

## User story 4 - Capability discovery

As a campaign planner, I run only integrity protocols whose normative artifacts, implementation, and executable fixtures exist at the selected SHA.

### Acceptance scenarios

1. Given normative artifacts, source, and fixtures for a capability, when discovered, then it is `available` and its required campaign is listed.
2. Given only an announcement or contract placeholder, when discovered, then the capability is `unavailable` and its campaign is reasoned `skipped`.
3. Given missing evidence for one future capability, when another required capability is complete, then the future skip remains visible without blocking the available campaign.
4. Given a new SHA later exposes T-016 or signing, when selected, then a new manifest activates cases only from that SHA's ratified interface.

## User story 5 - Current global hash-chain conformance

As Matthias, I receive deterministic evidence that the selected SHA's existing global hash-chain implementation detects the failure classes it claims to detect.

### Acceptance scenarios

1. A valid canonical chain passes whole-chain verification.
2. Payload, schema version, source triple, idempotency key, event/ingestion/transaction time, trace ID, tags, predecessor, sequence, or record type tampering fails.
3. Wrong genesis, sequence gap, deletion, insertion, reorder, or linkage rewrite fails.
4. A caller-submitted reserved writer record type is refused according to the selected target boundary.
5. Append-only role tests refuse unauthorized update/delete and preserve the separate ingest/correction boundary.
6. Head-anchor export commits to the verified chain head.
7. A privileged actor rewriting and re-chaining the entire history without a trusted published anchor remains an explicit honesty limitation rather than a claimed pass.

## User story 6 - Capability-conditioned T-016 identity

As an evaluator of a future accessible SHA, I can activate identity cases without defining an interface before NEST ratifies it.

### Conditional acceptance scenarios

When the selected SHA exposes the ratified interface and fixtures:

1. Identical asset tags across deployments or sources never merge.
2. Sensor replacement preserves both old and new provenance.
3. Identity transfer is explicit and append-only.
4. Missing predecessors, cycles, conflicts, and cross-SPV collisions are refused exactly as ratified.
5. Dedup remains scoped to the full namespaced source identity.

At SHA `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`, these cases are `skipped/unavailable` because the implementation and fixtures are absent.

## User story 7 - Capability-conditioned Ed25519 signing

As an evaluator of a future accessible signed-chain SHA, I can independently test the ratified protocol without handling production private keys.

### Conditional acceptance scenarios

When the selected SHA exposes the ratified signing message, key lifecycle, implementation, and fixtures:

1. A valid signed record verifies using the target protocol and independent implementation.
2. Payload, record hash, predecessor, sequence, signature, algorithm, or key-ID tampering fails.
3. Wrong, unknown, retired, malformed, or missing public keys fail according to ratified epoch rules.
4. Missing, duplicate, malformed, or wrong-length signatures fail.
5. Insertion, deletion, reorder, replay, and backdated privileged append fail as specified.
6. A hash-valid re-chain without the private key fails signature verification.
7. Historical verification uses the public key valid for the recorded epoch.
8. Key compromise, administrator rewrite, and unsigned legacy behavior are reported within the target's ratified honesty boundary.

At the initial SHA, all cases are `skipped/unavailable`. RFC 8032, FIPS 186-5, and `cryptography` cannot define NEST's signing bytes or key policy.

## Functional requirements

- **NEF-002-FR-001:** A recorded campaign selector MUST be an `mN` gate tag or an explicitly acknowledged exact provisional commit SHA; mutable refs MUST be invalid.
- **NEF-002-FR-002:** Acquisition MUST use a clean detached disposable checkout under `.targets/nest/<sha>/` with no persisted credential.
- **NEF-002-FR-003:** Failure to access the requested revision MUST stop; NEF MUST NOT substitute `main` or another revision.
- **NEF-002-FR-004:** Optional local planning inspection MUST be read-only and record unchanged before/after status.
- **NEF-002-FR-005:** `TargetSnapshotManifest` MUST include every field required by its normative schema.
- **NEF-002-FR-006:** `TargetCapabilityManifest` MUST list available capabilities, required campaigns, and reasoned unavailable campaigns.
- **NEF-002-FR-007:** Capability activation MUST require normative artifacts, implementation, and executable fixtures at the same selected SHA.
- **NEF-002-FR-008:** Protocol digest construction MUST be deterministic and its input paths/digests recorded.
- **NEF-002-FR-009:** Current hash-chain conformance MUST cover canonical hashing, genesis, sequence, linkage, committed stored fields/source identity, reserved types, append-only permissions, whole-chain verification, and anchor export.
- **NEF-002-FR-010:** Current-chain sabotage MUST include individual field tamper, reordering, insertion, deletion, gap, genesis, linkage, and re-chain honesty cases.
- **NEF-002-FR-011:** T-016 cases MUST remain conditional until the selected SHA supplies its ratified interface and fixtures.
- **NEF-002-FR-012:** Ed25519 cases MUST remain conditional until the selected SHA supplies signing bytes, key lifecycle, implementation, and fixtures.
- **NEF-002-FR-013:** Production private keys and seed material MUST never enter NEF; tests use public and synthetic fixture keys only.
- **NEF-002-FR-014:** Capability absence MUST remain visible as `skipped` with a reason and MUST NOT count as pass.
- **NEF-002-FR-015:** A future selected SHA MUST receive a new snapshot/capability manifest and protocol partition before amendment.
- **NEF-002-FR-016:** Gate mode MUST default to the highest numeric `mN` tag and MUST NOT order tags lexically or by time.
- **NEF-002-FR-017:** Gate snapshots MUST record the gate name, tag-ref SHA, and peeled commit SHA. Peeling an annotated tag dereferences the tag object; peeling a lightweight tag is identity.
- **NEF-002-FR-018:** Provisional snapshots MUST be explicitly acknowledged and labelled `provisional`, `non-gate-evidence`, and `non-reproducible-baseline`; they MUST NOT contribute gate scoring.
- **NEF-002-FR-019:** Default gate failure MUST NOT silently fall back to provisional mode.
- **NEF-002-FR-020:** Gate pinning MUST compare against prior validated snapshots. A changed tag-ref or peeled commit MUST produce a `moved` violation snapshot, refuse campaign construction as `invalid`, and emit a deterministic candidate Finding with old/new evidence.
- **NEF-002-FR-021:** The prior-snapshot deletion weakness MUST remain explicit. Append-only/hash-chained snapshot-manifest history is the named NEF-T004/T005 hardening seam and is not implemented by NEF-T002.
- **NEF-002-FR-022:** `target-integrity/target-binding` MUST be required for every target even when the selected NEST SHA exposes no executable product-integrity capability.

## Historical provisional profile

- SHA: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`
- Constitution: 1.3.0
- Protocol digest: `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`
- Required: `target-integrity/global-hash-chain-v1`
- Available context: `t-014-state-projector`, `t-015-ingestion-gate`
- Unavailable: `t-016-namespaced-identity`, `ed25519-per-record-signing`

The `de8c077...` orientation predates this amendment and is retained as provisional/non-gate evidence. It is not retroactively promoted because no `m1` gate tag binds it.

## Current default gate profile

- Gate tag: `m0`
- Tag-ref SHA: `8362f666336c429812fbf32aabc8eaaf1d9ac47a`
- Peeled commit: `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`
- Mode/class: `gate-evidence`, `reproducible-baseline`
- Required: `target-integrity/target-binding`
- NEST product-integrity capabilities: unavailable at this scaffold/CI milestone; explicit reasoned skips
- `m1`: absent at the 2026-07-12 pin observation

## Edge cases

- A mutable selector carries a plausible resolved SHA: invalid before acquisition.
- `m10` and `m9` exist: select `m10`, never lexical `m9`.
- A lightweight gate tag has tag-ref SHA equal to commit SHA: valid identity peel.
- A prior annotated tag becomes lightweight at the same commit: moved tag because the tag-ref binding changed.
- Gate selection finds no eligible tag: refuse without provisional fallback.
- Remote resolution succeeds but checkout contains a different HEAD: error.
- Target checkout becomes dirty during inspection: harness error.
- Constitution says a capability exists but source/fixtures do not: unavailable with inconsistent-source evidence; never infer executable support.
- Source exists without ratified normative behavior: unavailable.
- Fixtures exist but are skipped or non-executable at the selected SHA: unavailable or inconclusive according to explicit evidence; never pass.
- Same target SHA with a different protocol input set: separate protocol digest and result partition.
- Prior snapshot deletion makes a moved tag appear first-seen: visible detection limitation, not pass evidence about immutability.

## Sabotage obligations

Target acquisition sabotage covers mutable selector rejection, numeric gate ordering, annotated/lightweight peeling, no-fallback behavior, moved tag-ref, moved peeled commit, missing prior history, wrong checkout SHA, dirty checkout, persisted credential, missing pinned revision, local-tree write detection, missing manifest fields, and false capability activation. Integrity sabotage covers every current-chain fault and, once available, every T-016/signing class.

## Success criteria

- **NEF-002-SC-001:** A manifest fully identifies the immutable selector, peeled target, evidence class, binding state, and environment with no moving-ref ambiguity.
- **NEF-002-SC-002:** Every current hash-chain sabotage fixture is detected with a non-pass state and evidence.
- **NEF-002-SC-003:** T-016 and signing are visible skips at the initial SHA and never appear in a pass denominator.
- **NEF-002-SC-004:** No target or original local checkout is modified.
- **NEF-002-SC-005:** Future capability activation can occur by new manifest/spec amendment without changing the public campaign seam.
- **NEF-002-SC-006:** Only valid gate-tag snapshots count as gate evidence; provisional runs remain visible and excluded from baseline scoring.
- **NEF-002-SC-007:** A moved previously observed gate tag is retained as evidence, refused as campaign input, and surfaced as a deterministic candidate finding.
