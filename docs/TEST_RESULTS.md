# Verification record

## Initial setup - 2026-10-27, America/Denver

Tester: JoshuaKosakowsky with Codex. Local environment: Windows, Python 3.12.14,
uv 0.12.19. Initial scaffold before publication:

| Check | Observed result |
|---|---|
| Locked environment / repository safeguards | Passed; required files present and no prohibited tracked paths |
| Ruff correctness checks | Passed |
| pytest | 4 passed; upstream Starlette/httpx deprecation warning, no failures |
| Chromium | Page load, refresh, reload, unavailable health and recovery passed; zero captured browser errors |
| Screenshot inspection | Plain title, setup notice and Running status verified |
| pip-audit | Passed; no known vulnerabilities reported for this platform's locked packages |
| Local source archive | Passed; isolated locked runtime and normal README launcher |
| GitHub exact-commit archive | Passed locally and in GitHub CI; isolated install, health, home and static assets |
| GitHub CI | Passed on initial published scaffold; all seven jobs succeeded |
| GitHub dependency audit | Passed on Windows/Python 3.12 and Linux/Python 3.12 and 3.14 |
| Collaborators / public settings | Public, default main, five pending Write invitations, main unprotected, zero rulesets |

Initial tested code commit: `87b14d57ecadbeb73fceeafd458801c6fcbeb5fa`.

- [Passing initial CI run](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/actions/runs/40622742267)
- [Passing initial dependency audit](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/actions/runs/40622742287)
- [Setup issue and subsequent verification](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1)

The locally downloaded exact-commit GitHub ZIP had SHA-256
`52017c1e20d33f6a04545a6e6211e3521c2c76487d45e04946092f58f4e248ae`.
It contained no Git metadata, `.env`, developer environment or local data. CI's
source-ZIP evidence artifact records its own observed archive hash. The local
pre-publication archive was recorded separately as a rehearsal.

These results identify the initial code commit. The final documentation-only
publication also triggers CI; its current result is recorded in the setup issue
to avoid changing a tested commit just to insert its own SHA. PR event handling
is configured but no independent human-reviewed PR is claimed during bootstrap.

Artifacts are ignored under `results/`. At this initial setup stage, no live
Calendar/OpenAI integration, business workflow, authentication or production
deployment had been tested. No keys or user data were used; main was unprotected.

## Baseline and protection verification - 2026-11-09, America/Denver

PRs [#22](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/pull/22)
and [#24](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/pull/24)
delivered the local/hosted job, report/CSV and course-model draft baseline.
Inventory, Ruff, 33 backend cases and normal-launch desktop/mobile Chromium passed;
all 10 checks passed on the reviewed application heads. Live course-model requests
were deliberate and bounded; CI used synthetic responses and made no provider calls.

[Deployment evidence #23](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/23)
records the Render/Neon launch at `c7e4879204634af5880567fde38ddd00a2f9e4f2`,
real hosted drafts, edited copying, sign-in/conflict recovery, record retention
after redeploy/15+ idle minutes, and the exact-commit clean ZIP install. The owner
tested manual, local AI and hosted flows. Independent human installation and
physical-phone testing remain unverified; idle access does not prove process suspension.

[Protection evidence #2](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2)
and [current settings](GITHUB_SETUP.md) supersede the unprotected setup snapshot.
Saved GitHub rules were read back through the API; security settings were verified
after reload. Existing PR #25 reports merging blocked. No destructive push/merge
test was attempted. These documentation changes do not establish a new deployed build.
