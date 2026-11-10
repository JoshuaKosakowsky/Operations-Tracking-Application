# Operations Tracking Application

A shared workday board for field-service and solar crews. Schedule a job, assign
a crew, record progress and work, then review a daily report and download its CSV.
The examples are fictional. This is a classroom prototype, not a payroll system.

## Install and run locally

Install Python 3.12 and run these commands from the extracted project folder:

```powershell
python -m pip install uv==0.12.19
python scripts/dev.py
```

Open <http://127.0.0.1:8000>. Stop with Ctrl+C. For another port use
`python scripts/dev.py --port 8001`. The launcher installs the exact `uv.lock`
dependencies. First installation needs internet; Git and Node are not required.
Windows uses a short environment under `%LOCALAPPDATA%/OTA`, not a Mac-synced
`.venv`. Mac/Linux use their own `.venv`.

## Use the app

1. Select a workday (all schedules use America/Denver / Mountain time).
2. Choose **Try example workday**, or **Add job** and enter a name, crew, site and time.
3. Select a job; update progress, elapsed crew minutes, miles, modules and notes.
4. **Save job**. Unsaved edits do not appear in reports. **Discard changes** restores
   the last loaded version; **Refresh** retrieves current team changes.
5. Open **Daily report** to review all crews for that date. **Download CSV** exports
   the saved records. Time is per job/crew, not per employee. Zero site time leaves
   the modules-per-hour figure unavailable.

If another person edits the same job first, the app rejects your stale save.
Copy any unsaved notes you need, refresh the job, and reapply your changes.
Delete requires confirmation and removes that job's data; there is no undo.

## Configuration and storage

No keys are needed for the local job workflow. Local records persist in the ignored
`data/operations.db` file, including across server restarts. Keep that file outside
Git and submission archives. CSV is a readable export, not a full restorable backup.

Optional configuration belongs in an ignored `.env` in the project root or in
environment variables. Existing environment variables take precedence. See
[.env.example](.env.example); never put secrets into browser code or screenshots.

| Setting | Purpose |
|---|---|
| `DATABASE_URL` | Local SQLite by default; PostgreSQL for durable hosting. |
| `TEAM_ACCESS_CODE` | Shared team sign-in; use at least 24 random characters for hosting. |
| `APP_ENV=production` | Requires durable PostgreSQL, a strong access code and HTTPS origin. |
| `APP_ORIGIN` | Exact hosted HTTPS origin, without a trailing slash. |
| `BUILD_SHA` | Exact source commit when packaging without Git metadata. |

Local passwordless access is limited to loopback. A configured access code enables
8-hour server-side sessions; sign-out revokes the session. Rotating the code revokes
old sessions. Everyone with the code can read, edit, export and delete all jobs.
This does not implement individual identities, role permissions or an audit trail.

## Current limitations

- GenAI is not connected. Customer-update and manager-summary controls are disabled;
  the app does not substitute canned text and call it AI.
- No shared hosted URL yet. Hosting account setup and durable database provisioning
  are pending. The same Python app and lock will serve both environments.
- Google Calendar, Maps and Bouncie are not connected. Scheduling, status, mileage
  and time are manual. There are no GPS-derived shifts, verified ETAs, maintenance
  predictions, payroll decisions or automatic customer messages.
- Use fictional data while evaluating. This is one team workspace, without backups
  or recovery beyond your own database backup. Do not use it for live operations.

## Verify and collaborate

Run `python scripts/dev.py --check` for inventory, Ruff and behavior tests.
[Testing commands](docs/TESTING.md) include desktop/mobile Chromium and fresh-ZIP
checks. [PLAN.md](PLAN.md) is the single outcomes/evidence checklist; human feedback
and independent testing remain distinct from automated checks.

[Team onboarding](docs/TEAM_ONBOARDING.md) · [GitHub project](https://github.com/users/JoshuaKosakowsky/projects/2)
· [Contributing](CONTRIBUTING.md) · [Agent rules](AGENTS.md)
· [Hermes reviewer policy](docs/HERMES_REVIEWER.md) · [Hermes setup](docs/HERMES_SETUP.md)

Branch/reviewer enforcement remains disabled per the owner's instruction. Existing
CI and eligible review remain the delivery practice. No license has been selected.
