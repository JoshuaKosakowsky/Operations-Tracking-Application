# Project plan

Initial scope approved 2026-10-27 (America/Denver): a new public repository, collaboration
documentation, FastAPI startup skeleton, CI and five collaborator invitations.
No product features or design decisions are included. Assignment 3 is a workflow
reference only; this repository starts with fresh Git history.

Planning authorized 2026-11-08: create issues, native sub-issues and a GitHub Project
around the professor's feedback. The proposal is sufficient to begin development;
the immediate priorities are proving external API access and enabling reproducible
professor evaluation. Class 9001+ endpoints are an optional development choice.
This tracking milestone does not establish completed integrations or provider tests.

## Milestones

| ID | Outcome and acceptance | State / owner |
|---|---|---|
| [SETUP-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Required docs, safe configuration, plain FastAPI startup, locked environment, relevant local checks and public GitHub CI | Complete / JoshuaKosakowsky with Codex |
| [SETUP-02](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Invite chha7734-web, jovi1214, mase7919, MSpanny and prse4479 with Write access; distinguish pending from accepted | Invitations sent; initially pending acceptance / JoshuaKosakowsky |
| [GOVERNANCE-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2) | Activate and verify strict main protection and independent-review requirements after owner authorization | Required later; deferred / unassigned |
| PLAN-01 | Translate the accepted proposal into feature acceptance, data ownership, integration ownership and task allocation | Future implementation planning / unassigned |
| [INTEGRATIONS-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/3) | Prove required external-service access: Google Maps [#6](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/6), Bouncie [#7](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/7) and Calendar [#8](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/8), with sanitized tests and evaluator prerequisites | See GitHub / unassigned |
| [LLM-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/4) | Assess the optional class endpoint route [#9](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/9), then configure and verify the selected provider [#10](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/10) | See GitHub / unassigned |
| [EVALUATION-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/5) | Prepare private evaluator credentials [#11](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/11), a rehearsed runbook [#12](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/12) and labelled sample/live coverage [#13](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/13) | See GitHub / unassigned |

## Tracking and dependency flow

The [Development & Evaluation Project](https://github.com/users/JoshuaKosakowsky/projects/2)
is public and linked to this repository. **Workflow** shows status and priority;
**Work breakdown** shows the native hierarchy, assignees and sub-issue progress.
Anyone can view the Project. Editing requires explicit Project Write access,
which is separate from repository access.

API access proof is P0; LLM and evaluator readiness are P1. Native dependencies
make #10 wait for the endpoint decision in #9, and final evaluation in #5 wait for
#3 and #4. Evaluation documentation can begin while these prerequisites are open.
The Project also includes completed setup #1 and deferred governance #2.

Keep each open issue's status label aligned with its Project status. Close parent
issues only when their sub-issues and stated integrated acceptance are complete.
GitHub owns live task status; these milestones describe the intended outcomes.

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
