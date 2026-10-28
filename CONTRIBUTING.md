# Contributing

This repository follows Assignment 3's collaboration structure with fresh history
and project-specific documentation. Agents also follow [AGENTS.md](AGENTS.md).

## Current workflow

Task branches, focused PRs and independent review are the intended practice.
Strict main blocking and mandatory reviewer enforcement are **not active yet**.
No protected-branch hooks or required checks/approvals are installed. The later
activation checklist is in [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).

1. Claim a substantial work item with concrete acceptance checks. Use one lead
   and up to two contributors (maximum three issue assignees). The lead owns
   acceptance and integration. Leave undecided ownership unassigned.
2. Branch from current `main`: `codex/<task>` for agents; human branches may use
   `feat/<slug>`, `fix/<slug>` or similar. Keep one substantial PR active per person.
3. Implement a focused behavior. Small related fixes stay with it; separate work
   when scope, interfaces or another contributor's ownership changes.
4. Run relevant checks, inspect the diff, update affected docs and `handoff.md`.
5. Open a PR describing the outcome, linked task and actual validation. Use
   `Refs #N` for partial work; `Closes #N` only when its acceptance checks are met.
6. Request an independent review, resolve findings and rerun affected checks.
   The approving reviewer or issue lead normally merges after validation.

## Creator and reviewer

Creators own their change, test evidence, safe handling and documentation.
Reviewers inspect correctness and user behavior, not test counts alone.
The author does not self-approve. A teammate with no commits on the PR is eligible
to review regardless of issue assignment. Current review rules are conventions;
GitHub will not enforce approval until the later activation milestone.

**Blocking findings:** broken required behavior, unsafe data/credential handling,
incompatible interfaces, failed relevant checks or unmet acceptance. State how to
reproduce and the expected result. Batch findings from the review.

**Non-blocking suggestions:** wording, style preferences, optional refactors and
out-of-scope improvements. Label them clearly and keep required work moving.

After a change to the reviewed code, review the relevant current head again.
If the original reviewer is unavailable, another independent teammate may verify
the fixes and document the evidence. Never imply the original reviewer approved
or silently dismiss an unresolved finding. Formal GitHub dismissal/protection
procedures will be defined when enforcement is activated.

## Integration and completion

Name an integration owner before multi-contributor feature work. Agree on shared
contracts and dependency/merge order first. A component PR may complete its own
checks while its parent feature stays open until the normal user flow works on
integrated `main`. Record environment, tester, commit, expected/actual results and
evidence. Skipped and mocked checks remain unverified for live integrations.

Each teammate should contribute meaningfully and review another teammate's work.
Record substantive implementation, review, testing and integration in
[docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md), without creating rows for routine edits.

## Labels and ownership

Every open work issue and PR uses one primary type and one current status.

| Type | Purpose |
|---|---|
| `bug` | Broken behavior |
| `enhancement` | New or improved feature |
| `documentation` | Instructions and evidence |
| `testing` | Tests and verification |
| `infrastructure` | Repository, CI, dependencies and deployment |

Statuses: `status: ready`, `status: in progress`, `status: blocked`,
`status: review`, `status: deferred`. Replace the previous status when it changes;
use closed/merged state for completion. Explain blockers and dependencies.
Do not invent assignees or create issues merely to apply a label.

## Records and private information

Issues own live task status; PLAN owns milestones and acceptance; README owns
setup/use; TEST_RESULTS owns evidence; handoff owns resumption. Update the affected
source rather than duplicating every change in every file.

Never publish keys, OAuth tokens, calendar/user data or unsafe logs in this public
repository. Keep example data synthetic. No license is selected yet.
