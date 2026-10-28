# Project plan

Scope approved 2026-10-27 (America/Denver): a new public repository, collaboration
documentation, FastAPI startup skeleton, CI and five collaborator invitations.
No product features or design decisions are included. Assignment 3 is a workflow
reference only; this repository starts with fresh Git history.

## Milestones

| ID | Outcome and acceptance | State / owner |
|---|---|---|
| [SETUP-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Required docs, safe configuration, plain FastAPI startup, locked environment, relevant local checks and public GitHub CI | Complete / JoshuaKosakowsky with Codex |
| [SETUP-02](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Invite chha7734-web, jovi1214, mase7919, MSpanny and prse4479 with Write access; distinguish pending from accepted | Invitations sent; initially pending acceptance / JoshuaKosakowsky |
| [GOVERNANCE-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2) | Activate and verify strict main protection and independent-review requirements after owner authorization | Required later; deferred / unassigned |
| PLAN-01 | Agree on operations-tracking requirements and acceptance, data ownership, integration owner and task allocation | Future planning / unassigned |
| INTEGRATIONS-01 | Plan Google Calendar authorization/data scope and OpenAI agent behavior, model, costs and safe action permissions | Future planning / unassigned |

## Setup acceptance

- Required root documents, templates, developer tooling and environment lock exist.
- Plain page and `/api/health` start without keys, `.env`, Git metadata or developer files.
- Python checks run on Windows/Linux; CI also exercises the documented newer runtime.
- Chromium smoke covers load, status refresh, reload and health error recovery.
- Exact-commit GitHub ZIP installs into an isolated environment and launches using README.
- Ruff uses a small correctness rule set; formatting remains advisory.
- Locked dependency audit runs on dependency changes, weekly and by manual dispatch.
- Public repository/`main`, collaborator invitation state, CI results and intentionally
  absent enforcement are verified and recorded without secrets.

## Later enforcement requirement

GOVERNANCE-01 is deliberately separate from working CI. Its acceptance includes
reviewing the future policy, enabling it only with authorization, and verifying
live server behavior. See [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).

## Future feature work

Define concrete user needs before choosing screens, database models, event-write
permissions, agent tools or automation. Name an integration owner and agree on
shared contracts before contributors implement dependent features. No invented
feature backlog or premature completion claim is part of this setup.

After publication, GitHub issues own live task states. Reconcile milestone
acceptance against actual evidence; component checks do not complete a parent flow.
