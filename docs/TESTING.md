# Testing

Run `python scripts/dev.py --check` for the locked inventory, Ruff and behavioral
tests. Windows uses the short environment selected by the launcher. Direct `uv`
commands should use that environment or a separate short-path environment, never
a `.venv` synced from another operating system.

## Browser and fresh package

```powershell
uv run --locked --group browser python -m playwright install chromium
uv run --locked --group browser python scripts/browser_smoke.py
uv run --locked python scripts/source_zip_check.py --sha FULL_COMMIT_SHA
```

Chromium uses an isolated fictional database and the normal launcher. It covers
team-code sign-in, examples, creation/editing, reload retention, daily report/CSV,
failed-save input retention and recovery, mobile widths and sign-out. Desktop and
390px mobile screenshots are under ignored `results/browser/`. This is automated
browser evidence, not human usability approval or live provider evidence.
AI UI tests substitute synthetic API responses; provider tests use HTTPX mock
transport. They cover unavailable/truncated/malformed responses, total timeout,
stale data, authentication, input bounds and durable usage limits. CI never calls
the course model. The browser also checks review-before-copy, draft editing,
plain-text rendering, unsaved-job gating and failed-generation recovery.

The ZIP check downloads the exact commit, rejects private/generated paths, extracts
without Git or `.env`, installs the same lock into a new environment, starts through
README's launcher, verifies the displayed build SHA, saves a fictional job and
checks its report. `--archive PATH` rehearses a local git archive before publication.
Git's `export-subst` stamps `operations_tracking/build.txt` in source archives.

## Provider and security checks

```powershell
uv run --locked --group audit python scripts/audit.py
```

Audit uses locked versions and reports failures without silently upgrading. CI keeps
the existing Python Windows/Linux matrix, Ruff, browser, source-ZIP and aggregate
`test` checks. The separate dependency audit runs on relevant changes and weekly.
Repository-required reviews/checks remain disabled per owner instruction.

Never run paid calls in startup, health, offline tests or CI. Integration checks
must be bounded, deliberate and documented separately from synthetic providers.
Keep credentials, real customer/employee records and screenshots of them out of
Git and artifacts. Use [PLAN.md](../PLAN.md) for acceptance evidence and blockers.

## Human delivery rehearsal

Give a second person the exact source ZIP and README. Record their identity, OS,
commit, installation result, workday/AI task results and any help required. The
owner's successful test and automated clean extraction do not satisfy independent
testing. Rehearse hosted desktop/mobile access, first request after inactivity,
provider errors and persistence after a redeploy before declaring delivery ready.
