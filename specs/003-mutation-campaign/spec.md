# Feature specification: Mutation campaign

**Spec:** NEF-003
**Status:** Approved for NEF-T001 implementation
**Depends on:** NEF-001, NEF-002

## Goal

Demonstrate whether the selected NEST test suite kills realistic bounded defects in explicitly included source, while publishing a complete and honest mutant denominator.

## User story 1 - Explicit mutation scope

As a maintainer, I can see exactly which files/operators were eligible and which source remained outside the campaign.

### Acceptance scenarios

1. Given a selected SHA, when mutation starts, then a versioned inclusion manifest enumerates files, exclusions, operators, tool version, and configuration digest.
2. Given source not in the manifest, when the tool discovers it, then it remains untested and cannot enter the denominator silently.
3. Given a capability-conditioned target path is absent, when scope is built, then it is a visible unavailable case rather than an empty successful shard.

## User story 2 - Disposable bounded execution

As an operator, I know mutants cannot contaminate the selected target or run beyond their declared budget.

### Acceptance scenarios

1. Each mutant runs in a disposable worktree derived from the exact target SHA.
2. Mutant shards respect job, process, time, memory, and output limits.
3. A timed-out mutant is `timeout` evidence normalized to a non-pass case state, never counted killed.
4. A mutation tool crash is a campaign error and remains distinct from a surviving mutant.

## User story 3 - Complete denominator and survivor evidence

As Matthias, I receive counts and evidence for every generated mutant.

### Acceptance scenarios

1. Every generated mutant is exactly one of killed, survived, timeout, invalid, or untested.
2. The sum of categories equals the generated total and duplicate mutant IDs are refused.
3. Every survivor retains patch, location, operator, exact test command, exit data, target SHA, environment, and evidence digest.
4. Invalid mutants record the validation reason and do not improve the mutation score.
5. Untested mutants remain in the denominator report with their reason.

## Functional requirements

- **NEF-003-FR-001:** NEF-T006 MUST select a maintained mutation tool from current primary evidence and lock its version.
- **NEF-003-FR-002:** Campaign scope MUST be an explicit versioned inclusion manifest; discovery alone cannot expand scope.
- **NEF-003-FR-003:** Mutants MUST be stable IDs derived from target SHA, file, operator, location, and normalized change, excluding run attempt.
- **NEF-003-FR-004:** Each mutant MUST execute in a disposable target worktree and MUST NOT modify the selected detached checkout or original NEST tree.
- **NEF-003-FR-005:** Shards MUST remain within declared workflow and campaign budgets.
- **NEF-003-FR-006:** Results MUST separately report killed, survived, timeout, invalid, and untested mutants.
- **NEF-003-FR-007:** The category sum MUST equal the generated total; missing results make the campaign inconclusive or error, never pass.
- **NEF-003-FR-008:** Mutation score MUST state its numerator and denominator and MUST NOT treat timeout, invalid, or untested as killed.
- **NEF-003-FR-009:** Every survivor MUST link to replayable evidence and the exact tests that failed to kill it.
- **NEF-003-FR-010:** Baseline target tests MUST pass before mutant grading; baseline failure is a harness/precondition error.
- **NEF-003-FR-011:** Integrity verification paths MUST be included only when the capability manifest declares them available.
- **NEF-003-FR-012:** T-016 and Ed25519 mutation paths MUST remain reasoned skips at the initial target SHA.
- **NEF-003-FR-013:** Model judgment MUST NOT determine mutant killed/survived status.
- **NEF-003-FR-014:** Raw tool output and per-mutant evidence MUST be sealed before aggregation.

## Outcome-to-state mapping

| Mutation outcome | Canonical case state | Meaning |
|---|---|---|
| killed | `pass` | The declared target tests detected the mutant. |
| survived | `fail` | The declared tests completed without detecting the mutant. |
| timeout | `inconclusive` | This mutant exhausted its declared per-mutant budget; it is not killed. |
| invalid | `invalid` | The generated change could not form a valid executable mutant. |
| untested | `skipped` | The mutant was generated but deliberately not executed; a nonempty reason is required. |

A campaign/job-level timeout, tool crash, cancellation, missing shard, or missing result is `error`. Any required mutant case that is timeout, invalid, or untested prevents the mutation campaign from passing under the shared aggregation rule.

## Edge cases

- Tool reports success but omits mutant results: error.
- Mutant does not compile or collect: invalid with evidence, not killed.
- Test runner times out after partially failing: timeout, not killed.
- Equivalent mutant cannot be proven automatically: survived or needs human disposition; never silently invalidated.
- Duplicate or nondeterministic mutant IDs: campaign error.
- Shard cancellation: missing results remain visible and the campaign cannot pass.

## Sabotage obligations

Seed at least one defect that the target suite must kill and one controlled survivor fixture whose evidence path is known. Sabotage missing denominator entries, duplicate IDs, timeout misclassification, invalid-as-killed inflation, worktree leakage, and absent survivor evidence.

## Success criteria

- **NEF-003-SC-001:** Complete denominator equality holds for every shard and aggregate.
- **NEF-003-SC-002:** Every survivor has a replayable evidence bundle.
- **NEF-003-SC-003:** Controlled killed and survived sabotage paths are classified correctly.
- **NEF-003-SC-004:** Target and original NEST trees remain unchanged.
- **NEF-003-SC-005:** Capability-conditioned paths are visible and never counted as passes when unavailable.
