# NEF trust model

## Assets

- Exact NEST source revision and its provenance.
- NEF source, schemas, campaign configuration, prompts, and protocol digest.
- Raw campaign inputs, outputs, logs, minimized examples, measurements, and usage records.
- Sealed evidence manifests, deterministic reports, findings, and human dispositions.
- Provider credentials and GitHub publication credentials.

Production signing keys, customer data, and customer evidence are forbidden assets: they must never enter NEF.

## Adversaries and failure classes

- Malicious or malformed target source, tests, specifications, fixtures, and workflow text.
- Prompt injection embedded in source or model responses.
- Product defect in NEST.
- Harness defect, timeout, cancellation, missing artifact, or corrupted evidence.
- Compromised target writer, database administrator, repository administrator, runner, provider, or hosting platform.
- Accidental secret inclusion, overbroad permissions, stale pricing, or budget overrun.

NEF distinguishes these classes; it does not reinterpret every anomaly as a product failure.

## Trust boundaries

```text
gate tag or acknowledged commit SHA
  -> pin-target (read-only; prior-binding comparison)
  -> exact SHA + TargetSnapshotManifest + TargetCapabilityManifest
  -> execute-* (disposable target, no provider secret, no repo write)
  -> sealed evidence
  -> aggregate (no target execution, no provider secret)
  -> validated deterministic report
  -> publish (minimal contents/issues write, no target execution)

validated secret-scanned source bundle
  -> audit-model (provider secret, no repo write, never executes source)
  -> sealed raw response
  -> candidate finding
  -> human triage and dated disposition
```

## Boundary rules

### Target acquisition

- Treat repository locators, tags, source, tests, documentation, issues, logs, and fixtures as untrusted data.
- Default to the highest numeric `mN` gate tag and record tag-ref plus peeled commit SHA; peeling a lightweight tag is identity.
- Permit provisional work only from an explicitly acknowledged commit SHA and label it non-gate evidence/non-reproducible baseline.
- Reject branches, `HEAD`, aliases, and other mutable recorded selectors. Never fall back silently from gate selection to provisional.
- Compare gate bindings with prior validated snapshots. Retain/refuse a moved binding and emit a deterministic candidate finding.
- Use `.targets/nest/<sha>/` as a detached disposable checkout.
- Verify the checkout is clean and contains no persisted credential material.
- Never execute in Matthias's original local NEST working tree.
- Record local checkout status before and after optional planning inspection.

### Target execution

- No provider secret, GitHub write token, customer data, or production key material.
- No route to modify NEST or its remote.
- Explicit file and command allowlists; bounded CPU, memory, time, and output.
- Any write is confined to the disposable workspace and NEF-owned ephemeral output.

### Model audit

- Input is a size-bounded allowlisted manifest, secret-scanned and delimited as untrusted data.
- Target code is never executed.
- The job has a provider credential but no repository write permission.
- Provider, model snapshot, request parameters, prompt/input/schema/SDK digests, usage, latency, and raw response are sealed.
- Model output emits `supported` or `suspected` candidates only.

### Evidence and aggregation

- Seal raw evidence before grading.
- Content-address every blob and validate every referenced digest.
- Treat only a manifest created after its validated blobs and retention record as sealed; consume
  only `VerifiedEvidence` at the later grading seam.
- Aggregation consumes only validated manifests.
- Missing or malformed evidence produces a non-pass state.
- Reports are deterministic projections and cannot upgrade candidate authority.

### Publication

- Publisher consumes validated canonical data and executes no target or PR-authored code.
- Grant only the exact contents/issues permissions required by the approved workflow.
- Stable fingerprints make recurrence idempotent.
- Publication failure is explicit and does not erase the underlying result.

## Key and data policy

- Credentials live only in environment variables or approved credential stores.
- Never place credentials on argv, in prompts, examples, config, logs, evidence, or repository files.
- Ed25519 testing uses RFC/NEST public data and synthetic fixture keys only.
- No production private key, seed, customer data, customer evidence, or production traffic.

## Honesty boundaries

- Current NEST hash chaining detects ordinary tamper and linkage faults, but a privileged actor can rewrite and re-chain history without a trustworthy published anchor.
- A GitHub evidence branch can be protected against normal force-push/deletion, but administrators or host compromise can still rewrite or delete it.
- The GitHub watchdog shares the scheduler's failure domain.
- Provider budgets are alerts, not hard caps.
- Model graders can be wrong; transcript and deterministic evidence remain available for human review.
- Contract validation rejects a `tag_binding.state` label that contradicts the previous/current SHA pair carried by the same snapshot, but it cannot prove that the supplied previous pair came from retained history. Moved-tag detection is only as strong as NEF-T005 pin-target comparison against that history; deleting a prior snapshot can downgrade a moved tag to `first-seen` and evade detection. The named future hardening seam is append-only/hash-chained snapshot-manifest history owned by NEF-T004/T005; NEF-T002 records this residual but does not build that history.
- Draft 2020-12 schema validation cannot enforce equality between instance fields or peel a Git object: a provisional `selector.pinned_sha` may differ from `resolved_sha`, and a gate `resolved_sha` may differ from `peel(tag_ref_sha)`, while remaining schema-valid. NEF-T003 contract-code validation rejects provisional inequality and requires verified annotated-tag peel evidence (with lightweight identity supported); NEF-T005 owns live Git peeling and supplies that evidence. Schema validity alone is not selector/SHA coherence evidence.
- Detectable-secret scanning rejects known forbidden paths, field names, private-key headers, and
  GitHub-token shapes, but cannot establish that arbitrary evidence is free of customer data or an
  unknown credential format. Producer allowlisting and the isolated T005 publisher remain required.
- T004's write-once canonical store is the substrate for snapshot history, not proof of its
  completeness. Until T005 adds discovery, prior-binding comparison, hash chaining, publication,
  and branch controls, moved-tag durability remains unimplemented.
