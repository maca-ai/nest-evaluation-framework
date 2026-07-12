# nest-evaluation-framework

NEF is a standalone, provider-neutral evaluation and verification framework for exact,
read-only NEST revisions. It preserves replayable evidence and publishes advisory findings;
it never modifies NEST or gates NEST merges.

## Development

Prerequisites: uv 0.11.28 or newer and a platform supported by its Python 3.12 distributions.

```sh
uv sync --locked --all-groups
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked mypy --strict src tests scripts
uv run --locked pytest
PYTHONPATH=src uv run --locked lint-imports
uv run --locked bandit -q -r src scripts
```

The disposable target directory is `.targets/`; it is always ignored and must contain only
detached exact-SHA checkouts. Never run a campaign in an original local NEST working tree.

Gate evidence defaults to the highest numeric NEST `mN` tag and records its tag-ref SHA plus
peeled commit SHA. Pre-gate work requires an explicitly acknowledged provisional commit SHA and
is always labelled non-gate evidence/non-reproducible baseline. Branches, `HEAD`, and moving refs
are never campaign selectors, and gate selection never silently falls back to provisional mode.

## Offline evidence verification

T004 evidence uses one canonical, content-addressed JSON store. Given a local store root and sealed
manifest digest, verification executes no target code and performs no network access:

```sh
uv run --locked python -m nef verify STORE_ROOT MANIFEST_DIGEST
```

Only a fully validated `VerifiedEvidence` result is eligible for later grading. The local layout,
400-day retention setup requirement, non-permanence boundary, and T005 publication/history seam
are documented in `docs/evidence-layout.md`.

## Trust boundary

Pull-request CI may execute PR code but receives no provider secret or repository write
permission. The spec-blind reviewer runs from trusted default-branch code after CI, fetches a
bounded PR diff as untrusted data, never checks out PR code, and emits advisory candidates only.
