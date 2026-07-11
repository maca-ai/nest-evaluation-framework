# NEF-T001 clarification record

**Run:** 2026-07-11
**Method:** Spec Kit clarify phase applied to the constitution, PRD, planning contract, six feature specifications, normative schemas, target profile, trust model, source matrix, and retention contract.

## Resolved questions

| ID | Question | Resolution | Authority |
|---|---|---|---|
| CL-001 | Does a moving target ref identify a run? | No. It is resolution input only; the exact SHA identifies the target. | PRD, PLANNING, Matthias 2026-07-11 |
| CL-002 | Does an unavailable capability block the whole run? | No. It is a reasoned visible skip when not required for that target; it is never a pass. | Constitution III/V, TASKS |
| CL-003 | Which state wins during aggregation? | Required error, then product fail, then required incomplete/non-pass to inconclusive, then pass only for complete required passes. | PLANNING, constitution III |
| CL-004 | Is model output a finding confirmation? | No. Model output creates `supported` or `suspected` candidates for human disposition. | AGENTS, PRD, constitution VIII |
| CL-005 | Can the first target use the unmerged VPS T-016 work? | No need. Matthias explicitly selected the accessible main baseline for NEF-T001. | Matthias 2026-07-11 |
| CL-006 | What is known about T-016 at the selected SHA? | The identity triple contract exists; the full identity-transfer/sensor-replacement implementation and fixtures do not. | Target snapshot search |
| CL-007 | What is known about Ed25519 at the selected SHA? | Constitution is 1.3.0; no ratified signing protocol, implementation, or fixtures exist. | Target snapshot search |
| CL-008 | Is 400-day artifact retention guaranteed? | No. It is requested only for a private repository when repository/organization limits permit it; setup fails otherwise. | GitHub primary documentation |
| CL-009 | Is the watchdog independent monitoring? | No. It shares GitHub's scheduling failure domain and is best-effort. | PLANNING, GitHub primary documentation |
| CL-010 | Are provider project budgets hard caps? | No. They are soft thresholds; NEF enforces its own conservative reservation ledger. | OpenAI primary documentation |
| CL-011 | Are Hypothesis seeds or opaque blobs durable replay evidence? | No. Durable minimized inputs are primary; blobs are exact-version supplements and the database is a cache. | Hypothesis primary documentation |
| CL-012 | Are JSON Schemas hand-authored implementation output? | No. They are normative T001 contracts; T003 generated schemas must conform semantically. | Approved NEF-T001 plan |
| CL-013 | Does current hash chaining defeat a privileged full rewrite? | Not without a trustworthy published anchor; this remains an explicit honesty boundary. | Selected target design record |
| CL-014 | May NEF create or use production signing keys? | No. Only public keys and synthetic fixture keys are permitted. | AGENTS, PRD, constitution X |

## Open but non-blocking evidence gaps

- `MISSING EVIDENCE`: T-016 identity-transfer message, predecessor model, conflict policy, and executable fixtures.
- `MISSING EVIDENCE`: Ed25519 signing bytes, key lifecycle, rotation, legacy behavior, privileged-append authorization, and executable fixtures.
- `MISSING EVIDENCE`: Whether the NEF repository/account currently permits 400-day retention; NEF-T005 must verify before enabling retention.
- `MISSING EVIDENCE`: Task-time model snapshots, prices, and SDK versions; NEF-T009 must refresh them before configuration.
- `MISSING EVIDENCE`: Maintained mutation tool choice; NEF-T006 selects it from current primary evidence.

These gaps are explicitly routed to capability discovery or later tasks. None is represented as success, and none requires inventing a protocol in NEF-T001.

## Clarify verdict

No unresolved critical clarification remains within NEF-T001's approved scope.
