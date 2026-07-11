# Feature specification: Adversarial model audit and quality checkpoint

**Spec:** NEF-006
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001, NEF-002

## Goal

Use a pinned model to inspect a bounded, secret-scanned NEST source manifest as untrusted data, retain the complete request/response evidence, and emit advisory candidates whose quality is calibrated against human dispositions.

## User story 1 - Safe bounded source bundle

As a security-conscious operator, I know exactly which source bytes left the target environment and that no target code executed in the model job.

### Acceptance scenarios

1. Given a selected SHA, when the bundle is built, then only explicit allowlisted text paths under size limits are included.
2. Given `.git`, environment files, credentials, artifacts, caches, binaries, generated data, or oversized files, when scanned, then they are excluded by default.
3. Given a secret-scan finding in otherwise valid source, when bundling occurs, then the campaign is `skipped` with evidence and no source is sent; a missing or failed scanner is `error`.
4. Given prompt injection in source, when submitted, then source remains delimited untrusted data and cannot alter system instructions or tool permissions.
5. The model job never executes target code and has no repository write permission.

## User story 2 - Pinned reproducible request

As an investigator, I can reconstruct the precise model interaction and its cost evidence.

### Acceptance scenarios

1. Provider, model snapshot, endpoint, request parameters, prompt/input/schema/SDK digests, usage, latency, and raw response are retained.
2. Given stale pricing or insufficient reserved allowance, when planning occurs, then the model campaign is `skipped` with reason before request.
3. Given provider outage or a response that remains malformed after bounded repair, when normalized, then the campaign is `error` and raw evidence is retained.
4. Given a schema repair attempt, when performed, then every raw attempt and validation error is retained within a bounded repair count.

## User story 3 - Candidate-only findings

As Matthias, I receive evidence-linked claims without model authority inflation.

### Acceptance scenarios

1. A model result may emit only `supported` or `suspected` candidates.
2. Every candidate includes source locations, claim, severity, reasoning summary, falsification attempt, and evidence references.
3. A deterministic contradiction downgrades or rejects candidate publication; model text cannot override deterministic evidence.
4. No candidate is called confirmed until human disposition.
5. Stable fingerprints exclude run IDs so recurrence updates one finding.

## User story 4 - Fourteen-day quality checkpoint

As Matthias, I can decide whether the model campaign earns daily cadence.

### Acceptance scenarios

1. Fourteen days after the first successful model-audit run, supported candidates are joined to dated human dispositions.
2. Confirmation rate uses an explicit numerator/denominator and excludes candidates without a disposition from confirmed counts while reporting them separately.
3. Under 50% confirmed defaults the cadence to weekly and reallocates allowance to fuzzing.
4. Another decision requires Matthias's dated disposition and a new protocol digest.
5. The checkpoint never changes NEST or promotes findings automatically.

## Functional requirements

- **NEF-006-FR-001:** Model input MUST be an explicit allowlisted, size-bounded, secret-scanned manifest from one exact target SHA.
- **NEF-006-FR-002:** Exclusions MUST cover `.git`, credentials, environment files, artifacts, caches, binaries, generated data, and oversized files by default.
- **NEF-006-FR-003:** Source and model output MUST be treated as untrusted data and MUST NOT expand instructions, permissions, or scope.
- **NEF-006-FR-004:** The model job MUST execute no target code and have no repository write permission.
- **NEF-006-FR-005:** Provider, pinned model snapshot, endpoint/request parameters, prompt/input/schema/SDK digests, usage, latency, times, and raw responses MUST be sealed.
- **NEF-006-FR-006:** Exact model, SDK, request schema, data controls, and pricing MUST be refreshed from primary sources at NEF-T009 decision time.
- **NEF-006-FR-007:** A single-writer monthly ledger MUST reserve conservative worst-case allowance before the request.
- **NEF-006-FR-008:** Stale pricing or insufficient allowance MUST yield `skipped`; provider budget alerts MUST NOT be treated as hard caps.
- **NEF-006-FR-009:** Repair attempts MUST be bounded and every raw response/validation error retained.
- **NEF-006-FR-010:** Model candidates MUST be `supported` or `suspected`, authority `candidate`, and evidence-linked.
- **NEF-006-FR-011:** Deterministic checks MUST precede and override probabilistic judgment where they conflict.
- **NEF-006-FR-012:** Finding fingerprints MUST exclude run identity and recurrence MUST be idempotent.
- **NEF-006-FR-013:** Fourteen days after the first successful run, the quality checkpoint MUST compare supported candidates with dated dispositions.
- **NEF-006-FR-014:** Under 50% confirmed MUST default cadence to weekly and reallocate allowance to fuzzing unless Matthias records another decision and protocol digest.
- **NEF-006-FR-015:** The campaign and checkpoint MUST NOT gate NEST, remediate it, or promote/close findings automatically.

## State mapping

- A valid completed audit with complete evidence and no supported/suspected candidate is `pass`; this means the bounded audit completed, not that NEST is defect-free.
- Evidence-backed candidate findings make their cases `fail` while remaining candidate authority.
- A detected source secret or insufficient reserved allowance is a reasoned `skipped` campaign before request.
- An empty valid bundle, insufficient human dispositions at the quality checkpoint, or non-reproducible candidate evidence is `inconclusive`.
- A malformed candidate citation/shape that is isolated without corrupting the campaign is `invalid` for that case.
- Scanner failure, provider outage, exhausted job timeout, malformed response after bounded repair, missing usage, or missing sealed evidence is `error`.

## Edge cases

- Bundle is empty after exclusions: invalid/inconclusive, not a clean audit pass.
- Secret scanner fails or is missing: error; no model request.
- Provider returns prose instead of schema: bounded repair or explicit error with raw response.
- Usage metadata is missing: evidence incomplete; campaign cannot pass.
- Candidate cites a nonexistent path or line: invalid candidate retained as grader evidence, not published as supported.
- Prompt injection asks for secrets, tools, or policy changes: ignored as data and captured in evidence.
- No dispositions at day 14: checkpoint reports insufficient evidence; it does not invent a confirmation rate.

## Sabotage obligations

Include planted defect, prompt injection, fake secret, oversized/binary path, malformed response, provider outage, exhausted allowance, stale pricing, missing usage, hallucinated source citation, duplicate finding, and low-confirmation checkpoint fixtures.

## Success criteria

- **NEF-006-SC-001:** A planted evidence-backed defect yields a candidate while injected instructions cannot alter behavior.
- **NEF-006-SC-002:** No excluded or secret-bearing content reaches the request manifest.
- **NEF-006-SC-003:** Every request/response is reconstructable from sealed metadata and raw evidence.
- **NEF-006-SC-004:** Model output never becomes authoritative or confirmed without human disposition.
- **NEF-006-SC-005:** The quality checkpoint computes the declared rate and applies the default cadence rule without automatic threshold promotion.
