# Feature specification: Property and stateful fuzz campaign

**Spec:** NEF-004
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001, NEF-002

## Goal

Exercise declared NEST surfaces with bounded generative and stateful properties, retain minimized durable failing inputs, and prove clean replay in the pinned environment.

## User story 1 - Capability-bound properties

As a campaign author, I generate only inputs for surfaces available at the selected SHA.

### Acceptance scenarios

1. Given an available target surface, when the campaign loads, then its property ID, input strategy, invariants, and capability dependency are versioned.
2. Given an unavailable surface, when planning occurs, then the property is a reasoned skip and does not run against an inferred interface.
3. Given T-014/T-015 available at the initial SHA, when selected for fuzzing, then their actual source contracts define the adapter rather than prose guesses.

## User story 2 - Durable minimized failure

As an investigator, I can reproduce the smallest retained counterexample without relying on an opaque seed alone.

### Acceptance scenarios

1. Given a property failure, when shrinking completes, then the minimized structured example is stored as durable case data.
2. Given a stateful failure, when retained, then the complete minimized operation sequence and preconditions are stored.
3. Given an opaque reproduction blob, when retained, then the exact Hypothesis/Python/test versions are recorded and the blob is supplemental.
4. Given only a seed, when no durable example exists, then the replay evidence is insufficient and the case cannot pass as reproduced.

## User story 3 - Clean pinned replay

As Matthias, I know whether a reported fuzz failure still reproduces from sealed evidence.

### Acceptance scenarios

1. Given a minimized example and pinned environment, when replayed in a fresh disposable checkout, then the same invariant fails and the case is `fail` with replay evidence.
2. Given replay no longer fails, when classified, then the result is `inconclusive`, not fixed or pass.
3. Given target, test, Python, or Hypothesis version mismatch, when replay starts, then it refuses or explicitly reports the mismatch.
4. Given a flaky target, when the same input produces inconsistent outcomes, then flakiness evidence is retained and the case is inconclusive.

## Functional requirements

- **NEF-004-FR-001:** Property/state-machine definitions MUST be versioned campaign data with stable IDs and capability dependencies.
- **NEF-004-FR-002:** Every run MUST declare max examples, stateful step count, deadline/timeout, memory, output, and randomness settings.
- **NEF-004-FR-003:** Failures MUST retain minimized structured examples; stateful failures retain minimized operation sequences.
- **NEF-004-FR-004:** Evidence MUST record target SHA, protocol/config digests, environment fingerprint, Python/Hypothesis versions, test identity, settings, and times.
- **NEF-004-FR-005:** Seeds, example databases, and `@reproduce_failure` blobs are supplemental and version-bound; they are not the sole durable replay source.
- **NEF-004-FR-006:** Every reported failure MUST replay from sealed durable data in the pinned environment.
- **NEF-004-FR-007:** Failed replay MUST be `inconclusive`; NEF MUST NOT call it pass, fixed, or confirmed.
- **NEF-004-FR-008:** Unavailable target surfaces MUST be visible reasoned skips.
- **NEF-004-FR-009:** T-016 properties MUST remain conditional and, once available, cover namespace collision, replacement, transfer, predecessor, cycle, conflict, and dedup scope according to the ratified interface.
- **NEF-004-FR-010:** Ed25519 properties MUST remain conditional and, once available, cover parsing, signature/key tamper, sequence/link/replay/re-chain, epoch, and legacy behavior according to the ratified interface.
- **NEF-004-FR-011:** Raw examples, shrink traces, logs, and replay results MUST be sealed before grading.
- **NEF-004-FR-012:** Model output MUST NOT grade property outcomes.

## Edge cases

- Hypothesis database entry disappears after upgrade: durable example still replays; otherwise inconclusive.
- Shrinking times out: retain best-known failing example and mark minimization incomplete without losing the failure.
- Generated input violates declared preconditions: invalid case, not pass.
- Test depends on external time/order/hash randomization: record flakiness and refuse a deterministic claim.
- Multiple distinct failures: retain separate stable case IDs and minimized examples.
- Campaign exhausts budget without sufficient examples: inconclusive with usage evidence.

## Sabotage obligations

Plant a property violation with a known shrink target, a stateful sequence failure, a flaky replay, an invalid generator case, an unavailable capability, and a version-mismatch replay. Prove each reaches the correct distinct state.

## Success criteria

- **NEF-004-SC-001:** Every retained failure has a durable minimized example or explicit incomplete-minimization evidence.
- **NEF-004-SC-002:** Clean pinned replay reproduces every graded failure; non-reproduction is inconclusive.
- **NEF-004-SC-003:** Seeds/blobs are never the sole correctness artifact.
- **NEF-004-SC-004:** Capability-conditioned T-016/Ed25519 cases are visible skips at the initial SHA.
- **NEF-004-SC-005:** Sabotage proves fail, invalid, inconclusive, error, and skipped paths.
