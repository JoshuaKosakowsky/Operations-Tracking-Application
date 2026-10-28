# Agent guide - Operations Tracking Application

Follow direct user instructions first. This guide applies throughout this repository.

## Start and finish

1. Read `handoff.md`; inspect branch, recent commits and working-tree changes.
   Verify inherited claims against the repository and preserve other people's edits.
2. Read the assigned task in `PLAN.md` or GitHub, then relevant acceptance checks.
   On first visit read README and CONTRIBUTING. Do not invent owners or issue IDs.
3. Make the smallest useful change, run relevant checks, inspect the diff and update
   affected docs. Update `handoff.md` before ending every session or switching models/agents.

## Current scope and authorization

- This is an approved fresh repository and FastAPI skeleton. Assignment 3 is a
  structural reference only; do not copy its code, features, providers or data.
- No operations-tracking features, UI design, database, Google OAuth connection or
  OpenAI API calls are authorized by the skeleton milestone.
- Initial repository creation, publication, setup commits, CI configuration and
  invitations for the five named collaborators are authorized by the owner.
  Subsequent work follows the user's authorization for that task; do not treat
  this setup authorization as permanent permission to publish unrelated changes.
- Preferred branches: `codex/<task>`. Use focused PRs and independent review as a
  team practice. Main protection, required approvals/status checks and blocking
  Git hooks are intentionally inactive. Never claim they are enforced.
- Activating strict main/reviewer enforcement is a later required milestone and
  requires owner authorization. Do not activate it during setup.

## Creator and reviewer responsibilities

- Creator: understand acceptance, coordinate shared contracts, implement within
  scope, run relevant checks, inspect safe files and document remaining gaps.
- Reviewer: independently assess correctness, security, acceptance and the user
  flow; give reproduction and expected behavior for a blocking finding.
- The author does not self-approve. A teammate with no commits on the PR is the
  intended reviewer, regardless of issue assignment. These are current team
  conventions; mandatory enforcement is deferred.
- Optional style/refactor suggestions are non-blocking. Do not waive unresolved
  correctness, security or required-acceptance findings merely to finish quickly.
- Fix routine reversible problems directly within the authorized task. Do not
  create an issue or approval request for every typo or missing import.
- Avoid speculative abstractions. Coordinate interface and shared-file changes
  before parallel implementation. Do not build against assumed unmerged code.

## Validation and data boundaries

- Run `python scripts/dev.py --check` for relevant Python changes. See
  `docs/TESTING.md` for browser, clean-ZIP and audit commands.
- Use normal-launch/browser evidence for user-flow claims. Mocks and passing
  backend tests do not establish a working external integration.
- No provider requests on startup, health refresh, CI or offline tests. Future
  live calls must be deliberate, bounded and authorized for the assigned task.
- Secrets stay server-side. Never commit keys, OAuth files/tokens or private user
  data, or expose them in browser code, logs, artifacts, screenshots or chat.
- Report implemented, tested and unchecked behavior accurately. Passing CI is
  evidence for its checks, not proof that the final project is complete.
- After checks pass, repeat them only for changed code, failures or unresolved risk.

## Mandatory short handoff

Keep the current entry around 15-25 lines: date/timezone and agent; task, branch
and base commit; changed files/decisions; commands, actual results and unchecked
areas; blockers; next 1-3 actions and links. Never include secrets or transcripts.

Preserve other contributors' pending notes. Use task-labelled entries for parallel
work; the integration owner consolidates on merge. Record a pre-handoff commit
instead of repeatedly amending a handoff to reference its own hash.
