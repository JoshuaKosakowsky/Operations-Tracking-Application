# Operations Tracking Application

Repository and FastAPI startup skeleton for the MBAX 6418 final project.

**Current scope:** team documentation, reproducible tooling, CI, a plain startup
page and a local health endpoint. Application features and visual design are pending.
Google Calendar and an OpenAI API agent are planned; neither integration is connected.
Assignment 3 supplied the workflow pattern only. This repository has fresh Git history.

Repository: [JoshuaKosakowsky/Operations-Tracking-Application](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application).

## Install and start

Use Python 3.12 (default) and uv 0.12.19. CI also checks Python 3.14 on Linux.
Python 3.12 is checked on Windows and Linux. Internet is needed for initial installation.

```powershell
python -m pip install uv==0.12.19
python scripts/dev.py
```

Open <http://127.0.0.1:8000>. Stop with Ctrl+C; choose another port with
`python scripts/dev.py --port 8001`. The launcher synchronizes `uv.lock` before
starting. It works from a clone or extracted source ZIP without Git or `.env`.
On Windows it uses a short environment path under `%LOCALAPPDATA%/OTA` to support
long OneDrive course paths. Set `UV_PROJECT_ENVIRONMENT` to override that location.

The page displays the app name and server health; Refresh status only calls
`GET /api/health`. FastAPI's API documentation is at `/docs`.
No API keys, accounts, database or Node installation are needed.
The development server binds to loopback; public deployment is a later decision.

## Verify

```powershell
python scripts/dev.py --check
```

Additional browser, clean-ZIP and dependency-audit commands are in
[docs/TESTING.md](docs/TESTING.md). Results and limits are in
[docs/TEST_RESULTS.md](docs/TEST_RESULTS.md). CI status is visible on GitHub;
it does not currently prevent merging.

## Work together

Read [CONTRIBUTING.md](CONTRIBUTING.md). Coding agents also read [AGENTS.md](AGENTS.md)
and [handoff.md](handoff.md). Use focused task branches and PRs, meaningful checks
and independent review as team practice. Main blocking and mandatory reviewer
enforcement are deliberately deferred; see [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).

[PLAN.md](PLAN.md) owns milestones and acceptance checks. GitHub issues own task
status once published. Keep ownership explicit and report implemented, tested and
unchecked behavior separately.

## Planned integrations and private configuration

[docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) records future Google Calendar and
OpenAI decisions. `.env.example` contains blank future settings only; this skeleton
does not load it or call either service. Keep keys, OAuth client files, tokens and
private data out of Git, CI artifacts, browser responses and public issues.

No license has been selected. Public visibility alone does not grant a license.
