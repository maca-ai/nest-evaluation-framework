# Evidence retention contract

## Evidence classes

| Class | Contents | Store | Retention intent |
|---|---|---|---|
| Raw bundle | Inputs, outputs, logs, minimized examples, raw measurements, model responses, environment and usage metadata | Private GitHub Actions artifact | Request 400 days only when supported |
| Validated manifest | Content addresses, sizes, media types, producer metadata, target/protocol/config digests, sealing time | Append-oriented evidence branch | Indefinite while repository exists, subject to hostile-host limitation |
| Deterministic report | Projection from validated manifests only | Append-oriented evidence branch | Same as validated manifests |
| Finding/disposition index | Stable fingerprint, recurrence references, dated human decisions | GitHub Issue plus canonical report data | Advisory lifecycle; no automatic closure/promotion |

## Sealing order

1. Campaign writes only to an isolated temporary bundle.
2. Publisher computes content digests and creates the evidence manifest.
3. Publisher atomically creates content-addressed objects without overwrite.
4. Offline verification checks sizes, digests, references, and manifest schema.
5. Only validated sealed evidence may be graded.
6. Reports are rebuilt deterministically from validated manifests.

Missing blob, digest mismatch, truncation, malformed manifest, duplicate conflicting write, or publication failure is explicit and never a pass.

## GitHub artifact retention

- Private GitHub repositories may support up to 400 days, subject to repository, organization, or enterprise policy.
- NEF-T005 MUST read and record the effective configured value before enabling the daily workflow.
- If the effective maximum is below 400 days, retention setup fails for human disposition; NEF does not silently request a shorter value.
- Retention changes do not retroactively extend existing artifacts.
- Workflow/run deletion can delete artifacts early; GitHub retention is not permanent storage.

## Evidence branch

- Machine-owned, append-oriented, and protected against force-push and deletion.
- Contains only canonical manifests, reports, and non-executable index data.
- Never merged into `main` and never used as an execution source.
- Publisher is its only runtime writer.
- Each publication uses idempotent paths derived from run identity and digest.
- Administrators or hosting-platform compromise can still rewrite or delete history; NEF states this limitation in reports.

The versioned local/branch tree is defined in `docs/evidence-layout.md`. NEF-T004 creates only the
local canonical files; NEF-T005 owns Git publication and protection.

## Privacy and exclusions

Evidence excludes credentials, environment files, production signing keys, signing seeds, customer data, customer evidence, and production traffic. Model inputs are allowlisted, size-bounded, and secret-scanned. Synthetic fixtures are clearly marked.

The local store rejects detectable forbidden paths, sensitive field names, private-key headers,
and GitHub-token shapes on write and verification. Pattern detection is not proof that arbitrary
content contains no customer data or unknown credential form; the producer allowlist remains a
required trust boundary.

## Verification obligation

An offline verifier must be able to validate a bundle using committed schemas and public metadata without executing target code or contacting a model provider. A scorecard or report with missing evidence is incomplete, never green.

`python -m nef verify STORE_ROOT MANIFEST_DIGEST` implements this local, network-free check. It
accepts only a canonical manifest created after its retention metadata and referenced blobs, and
returns nonzero for missing, malformed, non-canonical, or digest-inconsistent evidence.
