# Source availability matrix

The matrix determines whether a campaign is required for one exact target SHA. Normative artifacts define intended behavior, source shows an implementation, and executable fixtures prove a testable interface. Announcements alone never activate a campaign.

Current default gate target: annotated `m0` (`8362f666336c429812fbf32aabc8eaaf1d9ac47a` -> peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`). Historical `de8c077...` and `1e98933...` observations are provisional/non-gate evidence.

| Capability/input | Normative evidence | Implementation evidence | Executable evidence | Selected-SHA status | Campaign disposition |
|---|---|---|---|---|---|
| Target binding | NEF constitution 1.1.0; NEF-002 FR-001/016-022 | T002 normative schemas; T005 resolver later | T002 annotated/lightweight/moved/mutable vectors; T005 resolver sabotage later | Available | Required: `target-integrity/target-binding` |
| Global hash-chain v1 | NEST constitution 1.3.0 VIIIb; spec 001 FR-016 | implementation absent at m0 | executable chain fixtures absent at m0 | Unavailable | `skipped/unavailable`; normative text alone cannot activate it |
| T-014 state projector | spec 001 FR-006/017 | implementation absent at m0 | executable projector fixtures absent at m0 | Unavailable | Capability recorded unavailable |
| T-015 ingestion gate | spec 001 FR-003 | implementation absent at m0 | executable gate fixtures absent at m0 | Unavailable | Capability recorded unavailable |
| T-016 namespaced identity | spec 001 FR-005 | implementation absent at m0 | identity fixtures absent at m0 | Unavailable | `skipped/unavailable`; later provisional SHA evidence cannot be projected backward |
| Ed25519 per-record signing | Announced future constitution 1.4.0 only | Signing message, key registry/lifecycle, verifier, and migration absent | Target signing fixtures absent | Unavailable | `skipped/unavailable`; reason required; no interface invention |
| Mutation inclusion surface | NEF spec 003 | Not selected in T001 | Not present | Deferred | NEF-T006 selects explicit manifest and maintained tool |
| Property/stateful surface | NEF spec 004 plus target capability manifest | Target-specific adapters not implemented | Replay fixtures not present | Deferred | NEF-T007 conditions on target capabilities |
| Performance reference SHA | NEF spec 005 | Registry not implemented | No approved reference entry | Deferred | NEF-T008 requires human-approved reference |
| Model source bundle | NEF spec 006 | Allowlist/scanner not implemented | Planted-defect and malformed-response fixtures absent | Deferred | NEF-T009 implements after current model/pricing research |

## Discovery rules

1. In gate mode, select the highest numeric `mN` unless an explicit gate tag is supplied; record tag-ref and peeled commit SHA. Lightweight peeling is identity.
2. In provisional mode, accept only an acknowledged exact SHA; label it non-gate evidence/non-reproducible baseline.
3. Compare gate bindings with prior validated snapshots. A moved binding is evidence, not executable input; never fall back silently.
4. Acquire a clean detached disposable checkout.
5. Record repository/mode/selector/SHA/classes/binding, lock/constitution/protocol digests, environment, source digests, paths, and time.
6. Search the selected SHA for normative artifacts, implementation, and executable fixtures.
7. Mark a capability `available` only when its required evidence classes are present.
8. Require target-binding for every target; list other required or unavailable campaigns explicitly.
9. Missing evidence never maps to available or pass.

## T-016 conditional source rules

Activation requires a ratified namespaced-identity interface, implementation, and executable fixtures at one selected SHA. Once available, acceptance covers identical tags across namespaces, sensor replacement preserving provenance, explicit append-only transfer, missing predecessor, cycles, conflicts, cross-SPV collisions, and full-identity-scoped dedup. Exact record shapes and refusal semantics come only from that SHA.

## Ed25519 conditional source rules

Activation requires the target's ratified constitution/specification/design record, precise signing message, key lifecycle/rotation rules, implementation, and executable fixtures. RFC 8032, FIPS 186-5, and `cryptography` are independent verification references, not substitutes for the NEST protocol.
