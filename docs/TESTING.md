# Testing and evidence

## Standard checks

```powershell
python scripts/dev.py --check
```

This uses locked dependencies and runs repository inventory, Ruff and pytest.
On Windows the launcher uses a short environment path; direct `uv` commands below
use `.venv` by default. If a long checkout path causes native-package problems,
set `UV_PROJECT_ENVIRONMENT` to a short absolute directory outside the repository
before those direct commands. Initial dependency/browser installation needs internet.

## Browser smoke

```powershell
uv run --locked --group browser python -m playwright install chromium
uv run --locked --group browser python scripts/browser_smoke.py
```

On Linux CI uses `playwright install --with-deps chromium`. Real Chromium starts
the app over loopback, checks title/content, status refresh, reload and an injected
health failure followed by recovery. Uncaught JavaScript errors, console errors,
failed requests and HTTP errors fail the check. Artifacts are in `results/browser/`.
Future controls need their own behavioral checks when implemented.

## Source ZIP

After publishing a commit, substitute its full 40-character SHA:

```powershell
uv run --locked python scripts/source_zip_check.py --sha FULL_COMMIT_SHA
```

The checker downloads GitHub's archive for that exact SHA, checks paths, extracts
into a temporary directory and installs only locked runtime dependencies into a
separate environment. It removes inherited provider settings and Python environment
overrides, then runs the README launcher, checks health/home/static assets and
records archive SHA-256 and tested SHA under `results/source-zip/`.
The archive must contain no `.git`, `.env`, credentials, local data or environments.
It does not exercise future integrations or replace independent final-project acceptance.

A pre-publication `--archive PATH` run is explicitly a local rehearsal, not proof
of a GitHub download. PR CI checks the PR head SHA (not the synthetic merge SHA);
normal Python/browser CI checks GitHub's PR merge ref. Push CI checks the pushed SHA.
Source-ZIP CI uses no repository checkout or provider secrets to run untrusted code.

## Dependency audit

```powershell
uv run --locked --group audit python scripts/audit.py
```

Exports exact locked pins for all dependency groups and uses locked pip-audit
without fixing/upgrading packages. Platform markers select the current runner's
dependencies. CI audits Python 3.12 on Windows/Linux and Python 3.14 on Linux on
dependency/configuration changes, weekly (Monday 13:00 UTC), and manually.
Findings or incomplete audits fail; network/database errors must not be reported
as a clean audit. Results are in `results/audit/`. An audit cannot prove there are
no unknown vulnerabilities.

## CI and evidence boundaries

The `test` aggregate succeeds only when Python checks, Ruff, browser and source-ZIP
jobs succeed. Security audit is a separate workflow with dependency-path filtering.
There are no required merge checks or approvals yet. Keep status names stable for
the later enforcement milestone.

Record actual commands, environment, date, tested commit and expected/actual
results in TEST_RESULTS. Keep local artifacts ignored. CI uploads bounded failure
evidence and audit reports; no real credentials/user data are used in these checks.
Unit tests, mocks and skeleton CI do not establish live Calendar/LLM behavior.
Formatting is advisory; `uv run --locked ruff format --check .` is optional.
