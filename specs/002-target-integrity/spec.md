# Feature specification: Exact-SHA target integrity

**Spec:** NEF-002
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001 contracts, NEF constitution

## Goal

Resolve, acquire, fingerprint, and evaluate one immutable read-only NEST revision while conditioning integrity cases on capabilities that are actually ratified and executable at that SHA.

## User story 1 - Resolve and acquire exact source

As an evaluator, I know exactly which NEST revision was inspected and executed, independent of later branch movement.

### Acceptance scenarios

1. Given `NEST_REPO_URL` and `NEST_TARGET_REF`, when resolution succeeds, then the exact SHA is recorded before target-specific design or execution.
2. Given the remote ref changes after resolution, when the run executes, then it continues to use the recorded SHA rather than the new ref head.
3. Given the requested SHA cannot be fetched, when acquisition runs, then it stops with missing evidence and never substitutes another revision.
4. Given a disposable checkout, when inspected, then it is detached, clean, credential-free, and located under `.targets/nest/<sha>/`.
5. Given Matthias's original local checkout, when optional planning inspection completes, then its before/after status is identical and no target test ran there.

## User story 2 - Complete target provenance

As an investigator, I can reproduce why a capability was considered available for one target SHA.

### Acceptance scenarios

1. Given a selected SHA, when snapshot creation completes, then repository/ref/SHA, branch/tag, dirty state, NEF revision, lock/constitution/source digests, environment, consulted paths, and observation time are present.
2. Given an unborn NEF repository during bootstrap, when a snapshot is recorded, then `nef_sha` carries an explicit unavailable reason rather than a fabricated SHA.
3. Given a changed relevant source file at a future SHA, when the protocol digest is recomputed, then results partition from the previous protocol.

## User story 3 - Capability discovery

As a campaign planner, I run only integrity protocols whose normative artifacts, implementation, and executable fixtures exist at the selected SHA.

### Acceptance scenarios

1. Given normative artifacts, source, and fixtures for a capability, when discovered, then it is `available` and its required campaign is listed.
2. Given only an announcement or contract placeholder, when discovered, then the capability is `unavailable` and its campaign is reasoned `skipped`.
3. Given missing evidence for one future capability, when another required capability is complete, then the future skip remains visible without blocking the available campaign.
4. Given a new SHA later exposes T-016 or signing, when selected, then a new manifest activates cases only from that SHA's ratified interface.

## User story 4 - Current global hash-chain conformance

As Matthias, I receive deterministic evidence that the selected SHA's existing global hash-chain implementation detects the failure classes it claims to detect.

### Acceptance scenarios

1. A valid canonical chain passes whole-chain verification.
2. Payload, schema version, source triple, idempotency key, event/ingestion/transaction time, trace ID, tags, predecessor, sequence, or record type tampering fails.
3. Wrong genesis, sequence gap, deletion, insertion, reorder, or linkage rewrite fails.
4. A caller-submitted reserved writer record type is refused according to the selected target boundary.
5. Append-only role tests refuse unauthorized update/delete and preserve the separate ingest/correction boundary.
6. Head-anchor export commits to the verified chain head.
7. A privileged actor rewriting and re-chaining the entire history without a trusted published anchor remains an explicit honesty limitation rather than a claimed pass.

## User story 5 - Capability-conditioned T-016 identity

As an evaluator of a future accessible SHA, I can activate identity cases without defining an interface before NEST ratifies it.

### Conditional acceptance scenarios

When the selected SHA exposes the ratified interface and fixtures:

1. Identical asset tags across deployments or sources never merge.
2. Sensor replacement preserves both old and new provenance.
3. Identity transfer is explicit and append-only.
4. Missing predecessors, cycles, conflicts, and cross-SPV collisions are refused exactly as ratified.
5. Dedup remains scoped to the full namespaced source identity.

At SHA `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`, these cases are `skipped/unavailable` because the implementation and fixtures are absent.

## User story 6 - Capability-conditioned Ed25519 signing

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

- **NEF-002-FR-001:** A moving ref MUST resolve to an exact SHA before target-specific design or execution.
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

## Initial target profile

- SHA: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`
- Constitution: 1.3.0
- Protocol digest: `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`
- Required: `target-integrity/global-hash-chain-v1`
- Available context: `t-014-state-projector`, `t-015-ingestion-gate`
- Unavailable: `t-016-namespaced-identity`, `ed25519-per-record-signing`

## Edge cases

- Remote resolution succeeds but checkout contains a different HEAD: error.
- Target checkout becomes dirty during inspection: harness error.
- Constitution says a capability exists but source/fixtures do not: unavailable with inconsistent-source evidence; never infer executable support.
- Source exists without ratified normative behavior: unavailable.
- Fixtures exist but are skipped or non-executable at the selected SHA: unavailable or inconclusive according to explicit evidence; never pass.
- Same target SHA with a different protocol input set: separate protocol digest and result partition.

## Sabotage obligations

Target acquisition sabotage covers moving-ref race, wrong checkout SHA, dirty checkout, persisted credential, missing requested revision, local-tree write detection, missing manifest fields, and false capability activation. Integrity sabotage covers every current-chain fault and, once available, every T-016/signing class.

## Success criteria

- **NEF-002-SC-001:** A manifest fully identifies the selected target and environment with no moving-ref ambiguity.
- **NEF-002-SC-002:** Every current hash-chain sabotage fixture is detected with a non-pass state and evidence.
- **NEF-002-SC-003:** T-016 and signing are visible skips at the initial SHA and never appear in a pass denominator.
- **NEF-002-SC-004:** No target or original local checkout is modified.
- **NEF-002-SC-005:** Future capability activation can occur by new manifest/spec amendment without changing the public campaign seam.
