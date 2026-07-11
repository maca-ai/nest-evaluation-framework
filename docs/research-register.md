# Research register

Time-sensitive claims are refreshed from primary sources at decision time. Each entry states only the claim the source supports and the resulting NEF disposition. Missing evidence blocks the affected decision.

## 2026-07-11 - NEF-T001

| Source | Retrieved | Supported claim | Disposition |
|---|---|---|---|
| https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization | 2026-07-11 | Private repositories may configure Actions artifact/log retention from 1 to 400 days; organization or enterprise policy can impose a lower maximum; changes are not retroactive. | Request 400 days only after validating repository/account support; otherwise fail retention setup. |
| https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule | 2026-07-11 | Scheduled workflows run from the default branch and can be delayed or dropped during high load, especially near the start of an hour. | Schedule off-boundary, provide manual dispatch, and call the 26-hour watchdog best-effort rather than independent. |
| https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#setting-the-permissions-of-the-github_token-for-your-organization | 2026-07-11 | `GITHUB_TOKEN` permissions can be restricted and workflow `permissions` controls access. | Declare least privilege per job; separate target execution, model audit, aggregation, and publication. |
| https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository | 2026-07-11 | GitHub supports restricting allowed actions and documents full commit-SHA references. | Pin third-party actions by full SHA and validate workflow policy at NEF-T002/T005. |
| https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform | 2026-07-11 | OpenAI project monthly budgets are soft spending thresholds; requests continue after the threshold and alerts do not enforce a hard cap. | NEF uses a conservative application reservation ledger; stale pricing or insufficient allowance skips the model campaign. |
| https://platform.openai.com/docs/api-reference/usage | 2026-07-11 | The Usage API exposes project/model usage and the Costs endpoint is the financial reconciliation source. | Record usage/cost evidence, but do not treat provider alerts as enforcement. Exact endpoints and schema are rechecked at NEF-T009. |
| https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-07-11 | Agent evaluation should distinguish transcript and outcome grading; transcript review helps identify agent mistakes versus grader defects. | Keep deterministic outcome checks primary and retain model transcripts as candidate evidence for human calibration. |
| https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html | 2026-07-11 | Hypothesis stores and replays failures, but its database may be invalidated by version or test changes; explicit examples are preferred for durable correctness. | Retain minimized durable inputs as case data; treat databases as caches. |
| https://hypothesis.readthedocs.io/en/latest/reference/api.html#hypothesis.reproduce_failure | 2026-07-11 | `@reproduce_failure` blobs are tied to the exact Hypothesis version and are not guaranteed compatible across versions. | Record versions and blobs as supplemental replay metadata; a failed pinned replay is inconclusive. |
| https://github.com/github/spec-kit | 2026-07-11 | Spec Kit defines a constitution-led specify/clarify/plan/tasks/analyze workflow. | Apply the workflow without installing or vendoring a new tool in NEF-T001; store clarification and analysis results in-repo. |
| https://www.rfc-editor.org/info/rfc8032/ | 2026-07-11 | RFC 8032 describes Ed25519/Ed448 and provides test vectors; Ed25519 signatures are 64 bytes. | Use RFC test vectors with synthetic keys only after the target exposes a ratified signing protocol; RFC 8032 does not define NEST's signing message. |
| https://csrc.nist.gov/pubs/fips/186-5/final | 2026-07-11 | FIPS 186-5 is the current NIST Digital Signature Standard and includes EdDSA requirements. | Use as an independent cryptographic reference, never as a substitute for NEST's ratified message/key lifecycle. |
| https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/ | 2026-07-11 | The official `cryptography` hazardous-materials interface exposes Ed25519 key generation, sign, and verify operations with documented length/error behavior. | Lock and test the library at NEF-T002; use public and synthetic fixture keys only. |

## Deferred refresh points

- NEF-T002: Python, uv, Pydantic, quality tools, `cryptography`, action SHAs, and Anthropic review-model snapshot.
- NEF-T006: mutation-tool maintenance, supported Python versions, and licensing.
- NEF-T007: exact Hypothesis version and replay behavior.
- NEF-T009: OpenAI model snapshot, API request schema, SDK version, pricing, usage accounting, and data controls.

No pricing, model snapshot, mutation-tool selection, or repository retention setting is frozen by NEF-T001.
