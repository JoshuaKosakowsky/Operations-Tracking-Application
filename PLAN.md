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

## Delivery checkpoints - authorized 2026-11-09

The owner requested native GitHub milestones and plain-language tracking for the
whole team. [Project overview](https://github.com/users/JoshuaKosakowsky/projects/2/views/3?pane=info)
is the team starting point; [Milestone roadmap](https://github.com/users/JoshuaKosakowsky/projects/2/views/3)
groups every task by checkpoint. Workflow and Work breakdown remain available.

| Checkpoint | Date | Outcome / work |
|---|---|---|
| [1 - Connections ready](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/milestone/1) | November 16, 2026 - team planning target | Agree the demo/AI behavior (#14), confirm team access (#15), prove service access (#3, #6-#8), and verify the AI connection (#4, #9-#10). |
| [2 - First working demo](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/milestone/2) | November 30, 2026 - team planning target | Agree screens (#16), implement the useful AI result (#17), and verify the integrated workflow (#18; parent of #16/#17). |
| [3 - Ready to present and submit](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/milestone/3) | December 10, 2026 - course deadline | Evaluator readiness (#5, #11-#13), fresh-user testing (#19), slides/recording (#20), and final submission checks (#21). |

**Canvas deadline supplied by Joshua: Thursday, December 10, 2026 at 11:59 p.m.
America/Denver (Mountain Time).** GitHub milestone dates are day-level checkpoints;
the description and Project overview preserve the exact submission time. The
first two dates are internal planning targets, not additional course deadlines.

Eight new issues (#14-#21) include plain-language outcomes and acceptance checks.
Existing work keeps its acceptance; technical issues now start with a short plain-
language explanation. Native dependencies record prerequisites; #13 now waits for
#14, and #5 also waits for the integrated demo #18. Ownership remains unassigned
until the team chooses leads. Setup #1 remains complete; governance #2 remains
deferred outside the three delivery milestones. No protection or invitation changes
are authorized or performed by this tracking setup.

The first demo's exact included/deferred features and data contract still need
team agreement in #14. These milestones authorize tracking and planning, not
implementation of every feature in the proposal. Sample/live behavior, actual
validation, evaluator access and independent teammate testing remain distinct.

## Milestones

| ID | Outcome and acceptance | State / owner |
|---|---|---|
| [SETUP-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Required docs, safe configuration, plain FastAPI startup, locked environment, relevant local checks and public GitHub CI | Complete / JoshuaKosakowsky with Codex |
| [SETUP-02](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/1) | Invite chha7734-web, jovi1214, mase7919, MSpanny and prse4479 with Write access; distinguish pending from accepted | Invitations sent; initially pending acceptance / JoshuaKosakowsky |
| [GOVERNANCE-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2) | Activate and verify strict main protection and independent-review requirements after owner authorization | Required later; deferred / unassigned |
| [PLAN-01](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/14) | Agree the first demo, AI behavior, data ownership, integration lead and included/deferred features | See GitHub #14 / unassigned |
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

Owner decision reconfirmed 2026-11-09: keep formal enforcement inactive while
Joshua is the only active human contributor. A new owner instruction is required
before activation. The dedicated Hermes reviewer is a disclosed automated role;
its [policy](docs/HERMES_REVIEWER.md) and [setup record](docs/HERMES_SETUP.md)
are separate from repository-wide safeguards. See [team onboarding](docs/TEAM_ONBOARDING.md).

GOVERNANCE-01 is deliberately separate from working CI. Its acceptance includes
reviewing the future policy, enabling it only with authorization, and verifying
live server behavior. See [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).

## Future feature work

Define concrete user needs before choosing screens, database models, event-write
permissions, agent tools or automation. Name an integration owner and agree on
shared contracts before contributors implement dependent features. The first demo scope is decided in #14; implementation planning is tracked by
#16-#18. Their creation does not establish approved detailed behavior or completion.

After publication, GitHub issues own live task states. Reconcile milestone
acceptance against actual evidence; component checks do not complete a parent flow.
