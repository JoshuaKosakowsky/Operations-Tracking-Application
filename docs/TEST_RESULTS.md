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
| Local source archive | Pending rehearsal |
| GitHub exact-commit archive and CI | Pending publication |
| Collaborators / public settings | Pending publication |

Artifacts are ignored under `results/`. No live Calendar/OpenAI integration,
business workflow, authentication or production deployment has been tested.
No keys or user data were used. Main/reviewer enforcement remains deliberately inactive.
