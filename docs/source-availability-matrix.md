# Source availability matrix

The matrix determines whether a campaign is required for one exact target SHA. Normative artifacts define intended behavior, source shows an implementation, and executable fixtures prove a testable interface. Announcements alone never activate a campaign.

Initial target: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`.

| Capability/input | Normative evidence | Implementation evidence | Executable evidence | Selected-SHA status | Campaign disposition |
|---|---|---|---|---|---|
| Global hash-chain v1 | NEST constitution 1.3.0 VIIIb; spec 001 FR-016; T-013 design | deterministic serialization/hashing, eventlog records/schema/writer/verifier, migration 0001 | golden vector, field-tamper, DB tamper, permission, verifier CLI tests | Available | Required: `target-integrity/global-hash-chain-v1` |
| T-014 state projector | spec 001 FR-006/017; T-014 design | deterministic fold, DB runner, migration 0002 | rebuild byte-identity, idempotency, read-your-writes, fail-stop tests | Available | Capability recorded; target-specific integrity cases may use it when declared by a campaign revision |
| T-015 ingestion gate | spec 001 FR-003; T-015 design | deterministic gate and intake service | decision atomicity, quarantine, hostile input, chain verification, no-bypass tests | Available | Capability recorded; fuzz/mutation may condition on it |
| T-016 namespaced identity | spec 001 FR-005 and task announcement | Identity triple contract only; full module absent | Identity-transfer, replacement, conflict, cycle, and collision fixtures absent | Unavailable | `skipped/unavailable`; reason required; no interface invention |
| Ed25519 per-record signing | Announced future constitution 1.4.0 only | Signing message, key registry/lifecycle, verifier, and migration absent | Target signing fixtures absent | Unavailable | `skipped/unavailable`; reason required; no interface invention |
| Mutation inclusion surface | NEF spec 003 | Not selected in T001 | Not present | Deferred | NEF-T006 selects explicit manifest and maintained tool |
| Property/stateful surface | NEF spec 004 plus target capability manifest | Target-specific adapters not implemented | Replay fixtures not present | Deferred | NEF-T007 conditions on target capabilities |
| Performance reference SHA | NEF spec 005 | Registry not implemented | No approved reference entry | Deferred | NEF-T008 requires human-approved reference |
| Model source bundle | NEF spec 006 | Allowlist/scanner not implemented | Planted-defect and malformed-response fixtures absent | Deferred | NEF-T009 implements after current model/pricing research |

## Discovery rules

1. Resolve `NEST_TARGET_REF` to an exact SHA from `NEST_REPO_URL`.
2. Acquire a clean detached disposable checkout.
3. Record repository/ref/SHA, branch or tag, lock and constitution digests, environment, source digests, paths, and time.
4. Search the selected SHA for normative artifacts, implementation, and executable fixtures.
5. Mark a capability `available` only when its required evidence classes are present.
6. List the campaigns required by available capabilities.
7. List unavailable campaigns with explicit reasons.
8. Missing evidence never maps to available or pass.

## T-016 conditional source rules

Activation requires a ratified namespaced-identity interface, implementation, and executable fixtures at one selected SHA. Once available, acceptance covers identical tags across namespaces, sensor replacement preserving provenance, explicit append-only transfer, missing predecessor, cycles, conflicts, cross-SPV collisions, and full-identity-scoped dedup. Exact record shapes and refusal semantics come only from that SHA.

## Ed25519 conditional source rules

Activation requires the target's ratified constitution/specification/design record, precise signing message, key lifecycle/rotation rules, implementation, and executable fixtures. RFC 8032, FIPS 186-5, and `cryptography` are independent verification references, not substitutes for the NEST protocol.
