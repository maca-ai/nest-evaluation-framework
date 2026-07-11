# NEF v1 specification handoff

This directory contains NEF's executable specification set. `specs/.specify/memory/constitution.md` is binding; `AGENTS.md` is the operational control file.

## Specification map

| Spec | Owns | Primary implementation tasks |
|---|---|---|
| 001 framework contracts | Shared vocabulary, schemas, evidence ordering, aggregation, orchestration, findings, publication | NEF-T003, T004, T005 |
| 002 target integrity | Exact-SHA acquisition, provenance, capability discovery, global hash-chain checks, conditional T-016/Ed25519 cases | NEF-T005 |
| 003 mutation | Inclusion manifest, sharding, denominators, survivors | NEF-T006 |
| 004 property/fuzz | Properties, state machines, minimization, durable replay | NEF-T007 |
| 005 performance | Approved reference, paired trials, raw series, decision rules | NEF-T008 |
| 006 model audit | Source bundle, prompt-injection posture, candidate findings, budget reservation | NEF-T009, T010 |

## Build order

NEF-T001 freezes the normative behavior and version 1.0.0 schemas. NEF-T002 creates the reproducible scaffold and trusted CI. NEF-T003 implements the public contracts and campaign seam. Evidence, orchestration/integrity, and four weapons follow in task order. One task and one branch may be active at a time.

## Standing target profile

The initial profile is NEST SHA `de8c0772dcb1890bfbf7c2c449a4252f63e0807a`, constitution 1.3.0, protocol digest `a41f9890187c18153890645f1a3cf7fc038e25e3f0ed13fcbde06f9abda80e40`.

- Required: global hash-chain v1.
- Available context: T-014 state projector and T-015 ingestion gate.
- `skipped/unavailable`: T-016 namespaced identity implementation.
- `skipped/unavailable`: Ed25519 per-record signing and constitution v1.4.0.

No future interface is inferred from an announcement. A newly accessible ref receives a new exact-SHA snapshot and capability manifest before amendment.

## Authority and honesty

NEST specifications remain authoritative for NEST behavior; NEF records and tests their selected-SHA interface without reinterpreting canon. Model output is never authoritative. Missing evidence never passes. NEF is advisory and never modifies or gates NEST.
