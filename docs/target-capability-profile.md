# Initial NEST target capability profile

## Provenance

- Repository: `https://github.com/maca-ai/nest.git`
- Requested ref: `main`
- Exact SHA: `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`
- Commit time: `2026-07-10T20:53:33+02:00`
- Commit subject: `fix(core): Sol audit remediation — B1/B2/B3/C2/C3 (#18)`
- Target tree: `f265c07c60deb3921bf2680b1013804aa9cb5cca`
- Constitution: 1.3.0
- Constitution digest: `6ee91bfd6eb150ca73199f29a9b6dfa5085c9ebd619c6186b8ee59b6fd7ac47a`
- Lock digest: `5b6f7af0cd9f72e75e30a384ba0b95b809544032e91b283513784a6b29494186`
- Integrity protocol digest: `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`

The complete snapshot, source digest register, environment fingerprint, capability search, and consulted paths are recorded in `SESSION_LOG.md`.

## Available capabilities

### Global hash-chain v1

Required integrity campaign. Selected-SHA evidence supports:

- canonical UTF-8 sorted-key JSON and SHA-256 record hashing;
- one global chain and 32-byte zero genesis;
- gap-free sequence with position commitment;
- predecessor linkage;
- committed schema version, source triple, times, trace ID, payload, and tags;
- reserved writer-record-type refusal;
- distinct ingest/correction DB roles and append-only permission tests;
- duplicate-receipt evidence;
- whole-chain streaming verification;
- canonical head-anchor export.

Honesty boundary: without a trustworthy published anchor, a privileged actor can rewrite and re-chain history. This selected SHA has no Ed25519 authorization layer.

### T-014 state projector

Available context capability. The selected SHA contains a deterministic fold, DB runner, migration 0002, checkpoint binding, rebuild byte-identity, idempotency, read-your-writes, and fail-stop tests.

### T-015 ingestion gate

Available context capability. The selected SHA contains deterministic gate evaluation, atomic decision/observation or decision/quarantine writes, bounded hostile-input handling, mixed-intake chain verification, and a no-gateless-append check.

## Unavailable capabilities

### T-016 namespaced identity

State: `skipped/unavailable`.

The `SourceIdentity` triple contract exists, but the target task is pending and no ratified identity-transfer/sensor-replacement implementation or executable fixtures exist. NEF does not define the missing record shapes or refusal rules.

### Ed25519 per-record signing

State: `skipped/unavailable`.

The selected target is constitution 1.3.0. It has no ratified signing message, key lifecycle, rotation policy, legacy rule, implementation, or executable signing fixture. RFC 8032, FIPS 186-5, and `cryptography` are independent references only.

## Refresh rule

When a new NEST ref is supplied, resolve it to a new exact SHA, create a new snapshot and capability manifest, and amend this profile through the normal review process. Never mutate this profile to describe a moving ref retrospectively.
