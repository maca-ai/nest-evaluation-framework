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

- NEF-T006: mutation-tool maintenance, supported Python versions, and licensing.
- NEF-T007: exact Hypothesis version and replay behavior.
- NEF-T009: OpenAI model snapshot, API request schema, SDK version, pricing, usage accounting, and data controls.

No pricing, model snapshot, mutation-tool selection, or repository retention setting is frozen by NEF-T001.

## 2026-07-12 - NEF-T002

| Source | Retrieved | Supported claim | Disposition |
|---|---|---|---|
| https://www.python.org/downloads/release/python-31213/ | 2026-07-12 | Python 3.12.13 is the current 3.12 security release; 3.12 is security-fixes-only. | Pin Python 3.12.13 for the v1 scaffold and treat interpreter changes as lock/protocol events. |
| https://pypi.org/pypi/pydantic/json; https://pypi.org/pypi/PyYAML/json; https://pypi.org/pypi/httpx/json; https://pypi.org/pypi/opentelemetry-api/json; https://pypi.org/pypi/opentelemetry-sdk/json; https://pypi.org/pypi/cryptography/json | 2026-07-12 | Official registry metadata reported Pydantic 2.13.4, PyYAML 6.0.3, httpx 0.28.1, OpenTelemetry API/SDK 1.43.0, and cryptography 49.0.0 as current stable releases. | Pin exact direct runtime versions and commit the uv lock. |
| https://pypi.org/pypi/pytest/json; https://pypi.org/pypi/pytest-asyncio/json; https://pypi.org/pypi/hypothesis/json; https://pypi.org/pypi/ruff/json; https://pypi.org/pypi/mypy/json; https://pypi.org/pypi/import-linter/json; https://pypi.org/pypi/bandit/json; https://pypi.org/pypi/pip-audit/json | 2026-07-12 | Official registry metadata reported pytest 9.1.1, pytest-asyncio 1.4.0, Hypothesis 6.156.6, ruff 0.15.21, mypy 2.2.0, import-linter 2.13, bandit 1.9.4, and pip-audit 2.10.1. | Pin exact development versions and execute them from the shared uv lock. |
| https://pypi.org/project/jsonschema/4.26.0/ | 2026-07-12 | jsonschema 4.26.0 supports Python >=3.10 and implements JSON Schema validation including Draft 2020-12. | Approved development-only dependency for semantic validation of the amended normative schemas. |
| https://docs.astral.sh/uv/concepts/projects/sync/; https://docs.astral.sh/uv/reference/cli/ | 2026-07-12 | `uv lock --check`, `uv sync --locked`, and `uv run --locked` refuse lock drift rather than silently updating it. | Use locked/checking modes locally and in CI. |
| https://github.com/astral-sh/setup-uv/releases/tag/v8.3.2; https://github.com/actions/checkout/releases/tag/v7.0.0 | 2026-07-12 | Official releases resolve to setup-uv commit `11f9893b081a58869d3b5fccaea48c9e9e46f990` and checkout commit `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0`. | Pin full action SHAs with release comments. |
| https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1 | 2026-07-12 | Official release v8.30.1 publishes a Linux x64 archive and checksum manifest; archive SHA-256 is `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`. | Download the pinned binary in CI, verify checksum before execution, and avoid the licensed action/secret. |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions; https://platform.claude.com/docs/en/about-claude/models/overview; https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking | 2026-07-12 | `claude-fable-5` is a fixed canonical model ID, generally available, with always-on adaptive thinking; non-default sampling parameters are rejected. | Pin `claude-fable-5`, omit sampling parameters, bound output, and keep review advisory. |
| https://platform.claude.com/docs/en/build-with-claude/structured-outputs; https://platform.claude.com/docs/en/api/messages/create | 2026-07-12 | Messages requests require `max_tokens`; `output_config.format` accepts JSON Schema, while refusals/truncation can still produce non-schema output. | Request a closed JSON shape and independently reject non-`end_turn`, malformed, or non-candidate output. |
| https://docs.github.com/en/actions/reference/security/secure-use | 2026-07-12 | Privileged workflows must not check out untrusted PR code; `workflow_run` can separate unprivileged CI from trusted secret-bearing review. | Reviewer runs from trusted default-branch code after CI and consumes the bounded PR diff only as data. |
| https://github.com/maca-ai/nest.git | 2026-07-12 | Read-only tag enumeration returned only annotated `m0`: ref `8362f666336c429812fbf32aabc8eaaf1d9ac47a`, peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`; `m1` was absent. | Default gate target is m0. Post-m0 work requires explicit provisional SHA mode; no moving-main selection or fallback. |

Target-tag observations are point-in-time evidence and are rechecked at pin time. No claim that GitHub prevents tag movement is made; NEF compares bindings against retained validated snapshots.

## 2026-07-12 - NEF-T003

| Source | Retrieved | Supported claim | Disposition |
|---|---|---|---|
| https://pypi.org/project/pydantic/ | 2026-07-12 | PyPI verified Pydantic 2.13.4 as the current stable release and published provenance/hashes for that release. | Keep the existing exact `pydantic==2.13.4` pin and lock; no dependency or lock change is needed for T003. |
| https://pydantic.dev/docs/validation/latest/concepts/models/ | 2026-07-12 | `ConfigDict(frozen=True)` rejects model attribute reassignment but nested mutable values remain mutable. | Use frozen/forbid-extra models plus internal recursive container freezing and test deep immutability through the public contract interface. |
| https://pydantic.dev/docs/validation/latest/concepts/validators/ | 2026-07-12 | Whole-model validators enforce constraints that depend on multiple validated fields. | Enforce selector/SHA coherence, moved-binding refusal, manifest equality, and result state/evidence invariants in model validators without changing frozen JSON Schemas. |
| https://pydantic.dev/docs/validation/latest/concepts/json_schema/ | 2026-07-12 | `model_json_schema()` produces JSON Schema Draft 2020-12-compatible dictionaries and supports validation-mode generation. | Expose deterministic generated validation schemas and prove semantic conformance against the eight frozen normative schemas. |
| https://docs.python.org/3.12/library/argparse.html | 2026-07-12 | Python 3.12.13 provides `ArgumentParser`, required subcommands/options, type conversion, generated help, and deterministic invalid-argument exits. | Implement the T003 CLI with standard-library argparse only; add no CLI dependency. |
| https://github.com/maca-ai/nest.git | 2026-07-12 | Live read-only tag enumeration returned only annotated `m0`: tag ref `8362f666336c429812fbf32aabc8eaaf1d9ac47a`, peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`; no `m1` ref exists. | Pin T003 orientation to unchanged m0 gate evidence. Do not select newer work or provisional mode. |

No T003 decision requires a new dependency, schema version, protocol, target baseline, provider, or service.

## 2026-07-12 - NEF-T004

| Source | Retrieved | Supported claim | Disposition |
|---|---|---|---|
| https://docs.python.org/3.12/library/functions.html#open | 2026-07-12 | Python 3.12.13 binary `x` mode performs exclusive creation and raises `FileExistsError` when the destination already exists. | Never open a final content-addressed path with truncating write mode; treat an existing different object as a conflict. |
| https://docs.python.org/3.12/library/tempfile.html#tempfile.mkstemp | 2026-07-12 | `mkstemp()` creates a user-only temporary file without a creation race when the platform implements `O_EXCL`; callers own cleanup. | Stage canonical bytes securely in the destination directory, flush/fsync them, atomically link the completed file into its final write-once name, and always remove the temporary name. |
| https://docs.python.org/3.12/library/os.html#os.fsync; https://docs.python.org/3.12/library/os.html#os.link | 2026-07-12 | `fsync()` flushes a file descriptor to disk; `os.link()` creates a hard link at a distinct destination name. | Publish only fully flushed bytes and use same-directory hard-link creation so the final path is never partially visible or overwritten. Fail explicitly if the filesystem cannot provide the primitive. |
| https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization | 2026-07-12 | Private repositories can configure Actions artifact/log retention from 1 to 400 days; managing organization/enterprise policy may impose a lower maximum, and changes are not retroactive. | Persist a requested-400/effective-maximum metadata record and refuse sealing when the observed maximum is missing or below 400. T004 does not query or mutate GitHub settings; T005 supplies the observation. |
| https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts | 2026-07-12 | Workflow artifacts can be deleted before expiration and deletion is irreversible. | Never claim 400-day metadata or an evidence branch provides permanence; retain the hostile-host/deletion limitation. |
| https://github.com/maca-ai/nest.git | 2026-07-12 | Live read-only tag enumeration at 2026-07-12T14:29:11Z returned only annotated `m0`: tag ref `8362f666336c429812fbf32aabc8eaaf1d9ac47a`, peeled commit `cb1d0ba91ac09b724b3648ca5fd8e2f502a77f12`; no `m1` ref exists. | Keep T004 oriented to unchanged m0 gate evidence; no provisional fallback or newer target assumption. |

No T004 decision requires a new dependency, normative schema, protocol shape, provider, service, GitHub setting mutation, or target execution.
