# Feature specification: Paired performance campaign

**Spec:** NEF-005
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001, NEF-002

## Goal

Detect meaningful NEST performance regressions using comparable alternating paired trials, raw evidence, predeclared uncertainty rules, and human-approved references.

## User story 1 - Approved comparable reference

As Matthias, I control which immutable reference SHA and decision rule may be used.

### Acceptance scenarios

1. Given no approved reference for a target/protocol, when the campaign plans, then the campaign is `skipped` with an explicit reason and the required-campaign aggregator makes the run `inconclusive`.
2. Given an approved reference, when a run starts, then reference SHA, approval record, protocol digest, benchmark config, and absolute floors are recorded.
3. Given hash-only target and signed-chain reference, when comparison is requested, then it is refused as a protocol mismatch.

## User story 2 - Alternating paired trials

As an investigator, I can distinguish a target regression from runner drift.

### Acceptance scenarios

1. Given target and reference, when trials execute, then they alternate on the same runner under one environment fingerprint.
2. Given warm-up trials, when analyzed, then the predeclared warm-up rule excludes them symmetrically.
3. Given a runner/environment change mid-series, when detected, then the series is invalid or inconclusive rather than merged.
4. Given insufficient or noisy pairs, when the decision rule runs, then the result is inconclusive.

## User story 3 - Raw series and honest decision

As Matthias, I can inspect every paired observation and reproduce the decision.

### Acceptance scenarios

1. Raw per-trial times, ordering, inputs, exit state, resource data, and environment are sealed.
2. Decision calculations use Decimal strings or integer base units without float-bearing hashed data.
3. A controlled slowdown crosses the predeclared rule and produces fail.
4. A target below an absolute floor fails even if relative comparison is noisy.
5. Historical VPS measurements appear only as non-comparable context unless fingerprints match.

## Functional requirements

- **NEF-005-FR-001:** Reference SHAs, protocols, benchmark configs, absolute floors, and decision rules MUST be human-approved and versioned.
- **NEF-005-FR-002:** Reference and target MUST execute as alternating paired trials on the same runner.
- **NEF-005-FR-003:** Raw series MUST retain trial order, role, measurements, warm-up flag, input/config digest, exit state, and environment fingerprint.
- **NEF-005-FR-004:** The campaign MUST predeclare warm-up, minimum pair count, noise/uncertainty, outlier, and decision rules before measurements.
- **NEF-005-FR-005:** Insufficient samples, excessive noise, environment drift, or incomplete pairs MUST produce `inconclusive` or `invalid`, not pass.
- **NEF-005-FR-006:** Threshold-compared and hashed values MUST use integers or Decimal strings, not floats.
- **NEF-005-FR-007:** Results MUST partition by target SHA, reference SHA, environment fingerprint, protocol digest, and benchmark configuration digest.
- **NEF-005-FR-008:** Historical measurements MUST be labeled non-comparable context unless fingerprints and protocol match the predeclared comparability rule.
- **NEF-005-FR-009:** Baselines, floors, uncertainty rules, and thresholds MUST NOT promote automatically.
- **NEF-005-FR-010:** Signing/verification overhead MUST be measured only when both target and approved reference expose comparable signed protocols.
- **NEF-005-FR-011:** Raw measurement and resource evidence MUST be sealed before the decision is computed.
- **NEF-005-FR-012:** Model output MUST NOT grade performance.

## State mapping

- A completed comparable series crossing the regression/floor rule is `fail`.
- A completed comparable series meeting all predeclared rules is `pass`.
- Insufficient/noisy/incomplete-but-valid pairs within the completed campaign budget are `inconclusive`.
- Environment or protocol mismatch makes affected cases `invalid`.
- No approved reference is a reasoned campaign `skipped`; because performance is required, run aggregation is `inconclusive`.
- Reference failure, runner/tool failure, job timeout, cancellation, or missing evidence is `error`.

## Edge cases

- Reference fails its own benchmark: error/precondition failure, not target pass.
- One half of a pair times out: incomplete pair retained; decision follows predeclared non-pass rule.
- Runner throttling or hardware change: environment partition or inconclusive.
- Target improves relative performance but violates an absolute floor: fail.
- Very fast measurements below timer resolution: invalid benchmark configuration.
- Signed capability appears only on target: no cross-protocol comparison; visible skip.

## Sabotage obligations

Inject a controlled slowdown, noisy series, missing pair, environment change, absolute-floor violation, and protocol mismatch. Prove deterministic classification and raw-series retention.

## Success criteria

- **NEF-005-SC-001:** Controlled slowdown is detected under the predeclared rule.
- **NEF-005-SC-002:** Noisy or insufficient series is inconclusive, never pass.
- **NEF-005-SC-003:** Every decision can be rebuilt from sealed raw paired series.
- **NEF-005-SC-004:** Historical incomparable measurements are clearly separated.
- **NEF-005-SC-005:** No baseline, threshold, or protocol promotion occurs without dated human disposition.
