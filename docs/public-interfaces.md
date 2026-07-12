# Public interfaces and schemas

Contract versions are per object. `TargetDescriptor`, `TargetSnapshotManifest`, and `CampaignRequest` are `2.0.0`; unaffected contracts remain `1.0.0`. Normative JSON Schemas live under `specs/001-framework-contracts/contracts/`.

## Deep execution seam

```text
Campaign.execute(CampaignRequest) -> CampaignResult
```

Implementations may be synchronous or asynchronous internally, but callers and conformance tests use this semantic seam. A campaign receives all target, capability, configuration, budget, and workspace inputs explicitly and returns state, measurements, candidates, replay metadata, and one sealed-evidence reference.

## Contract invariants

- Immutable after validation.
- Unknown fields refused.
- `schema_version` is semantic and object-specific; breaking target-pinning changes use 2.0.0.
- Timestamps are timezone-aware UTC strings.
- SHA-256 values are lowercase 64-character hexadecimal strings.
- Decimal values are strings, never JSON numbers.
- Hashed and threshold-compared structures contain no floats.
- IDs are stable lowercase kebab-case tokens or UUIDs as specified.
- Missing required evidence cannot validate as a pass.

## TargetDescriptor

Describes one immutable pin decision and its observed exact result:

- `repository_url`
- `target_mode`: `gate-evidence` or `provisional`
- `selector`: closed gate-tag or pinned-SHA variant
- `resolved_sha`
- `observed_at`
- `source_kind`: `local` or `remote`

Gate selectors record `gate_tag` plus `tag_ref_sha`. Provisional selectors record `pinned_sha` plus explicit acknowledgement. Branches, `HEAD`, aliases, and other mutable refs cannot validate. `resolved_sha == peel(tag_ref_sha)` is a semantic invariant; peeling a lightweight tag is identity. A provisional `pinned_sha` must equal `resolved_sha`.

## TargetSnapshotManifest

Proves which target and environment were inspected:

- repository, target mode, immutable selector, and resolved SHA
- evidence class and baseline reproducibility
- tag-binding state and prior binding evidence, or null for provisional mode
- dirty state
- NEF SHA or explicit unavailable bootstrap reason
- target lock, constitution, and protocol digests
- relevant source digests
- environment fingerprint
- consulted paths and observation time

Only `gate-evidence` plus `reproducible-baseline` may count toward milestone scoring. Provisional snapshots are `non-gate-evidence` and `non-reproducible-baseline`. A `moved` snapshot is valid violation evidence but cannot be embedded in an executable CampaignRequest.

## TargetCapabilityManifest

Partitions campaigns for one target SHA:

- target SHA and protocol digest
- capability records with state and evidence references
- required campaign IDs
- unavailable campaign IDs with reasons

Capability states are `available` or `unavailable`. Unavailable campaign state is represented as `skipped`, with the reason retained.

## CampaignRequest

Contains:

- run identity and attempt
- campaign ID
- target snapshot and capability manifests plus their canonical digests
- campaign configuration digest
- explicit time/cost/resource budgets
- disposable workspace relative path
- randomness and replay inputs

The workspace must resolve beneath the NEF-owned disposable target root.
CampaignRequest 2.0.0 embeds TargetSnapshotManifest 2.0.0 and rejects `tag_binding.state=moved`.

## CampaignResult

Contains:

- campaign and case states
- start/end times
- measurements as Decimal strings or integer counts
- candidate finding fingerprints
- replay metadata
- budget use
- evidence-manifest digest

A `pass` requires an evidence-manifest digest and complete required cases. The aggregator revalidates this invariant rather than trusting the producer.

## EvidenceManifest

Lists content-addressed objects with path, media type, byte size, and SHA-256 plus target/protocol/config/environment and producer metadata. `sealed_at` precedes any grade timestamp.

## Finding

Stable fingerprint excludes run/attempt identity. Finding authority is `candidate`; source is deterministic or model. Model candidates are `supported` or `suspected`. Evidence references are mandatory.

## Disposition

Human-only dated decision:

- `confirmed`
- `rejected`
- `needs-more-evidence`
- `accepted-risk`
- `fixed`

It records actor, rationale, time, finding fingerprint, and evidence/run references. No campaign may create a disposition.

## Schema evolution

T003 generates Pydantic JSON Schemas that must conform semantically to these normative schemas. Ordering of `$defs` or descriptions is not semantic; field names, types, requiredness, enums, formats, and closed-object behavior are. A breaking change requires Matthias, a schema-version change, cross-artifact analysis, and a new NEF protocol digest when behavior changes. Per-object versions may differ; consumers must honor the embedded object's version.
