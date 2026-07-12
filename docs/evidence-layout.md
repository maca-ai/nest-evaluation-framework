# Evidence store and branch layout

NEF-T004 defines one local, canonical JSON store. NEF-T005 may publish the same tree to the
machine-owned evidence branch, but this module neither invokes Git nor writes a remote.

## Version 1 layout

```text
evidence/v1/
  blobs/sha256/ab/abcdef...json
  manifests/sha256/cd/cdef01...json
  bundles/cdef01.../retention.json
```

- A blob filename is the SHA-256 digest of its canonical JSON bytes. The first two hexadecimal
  characters shard the directory. `EvidenceObject.path` remains the logical name inside the
  bundle; it is not used as a filesystem path.
- A manifest filename is the SHA-256 digest of the unchanged `EvidenceManifest` 1.0.0 canonical
  JSON. Manifest presence is the bundle's seal marker.
- `retention.json` records the manifest digest, requested days, observed policy maximum, and the
  literal assurance `policy-intent-not-permanence`. It is metadata, not a permanence claim.

All final files are regular, non-symlink files. Writes stage canonical bytes in the destination
directory, flush them, then create the final name without overwrite. Repeating identical bytes is
idempotent. Different bytes at an existing final name are a conflict and remain untouched.

## Seal and verification order

`EvidenceStore.seal` validates every referenced blob first, writes retention metadata second, and
creates the content-addressed manifest last. A failure before the final step does not create a seal.
Only `VerifiedEvidence` returned by `seal` or offline `verify` is eligible for later grading.

Offline verification performs no target execution and no network access. It requires canonical
UTF-8 JSON, digest/address agreement, declared size agreement, a valid unchanged
`EvidenceManifest`, an honest retention record, and every referenced blob. Missing, truncated,
malformed, non-canonical, symlinked, or digest-mismatched evidence fails closed.

## Retention and data honesty

Sealing requires an observed maximum of at least 400 days and always records a 400-day request.
An absent or lower observation is a setup failure; the store never silently shortens it. GitHub
administrators or the hosting platform can still delete or rewrite retained data, so neither the
metadata nor an evidence branch is permanent storage.

The store rejects detectable private-key headers, GitHub token shapes, sensitive field names, and
forbidden paths such as `.env`. Pattern scanning cannot prove an input is free of customer data or
unknown secret formats. Producers remain responsible for an allowlisted, synthetic or otherwise
approved input set; T005 owns the publisher-side scan and workflow boundary.

## Append-only history seam

The write-once canonical blob primitive can store future target snapshot manifests without a
second digest path. T004 does not create a discovery index, compare prior tag bindings, hash-chain
snapshot history, protect a branch, or claim durable moved-tag detection. Those integration and
publication obligations remain NEF-T005 scope.
