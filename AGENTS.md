# Agent guide - Operations Tracking Application

Follow direct user instructions first. This guide applies throughout this repository.

## Role dispatch

The default role is a contributing agent, including classmates' Hermes coding
agents. Only Joshua's separately launched `operations-reviewer` profile,
authenticated as JoshKozy, follows [HERMES_REVIEWER.md](docs/HERMES_REVIEWER.md).
That profile never edits project files or handoff.md; its posted review is its
handoff. It may review, comment, give eligible verdicts and merge checked PRs.
Reading its policy does not select the role or authorize credential switching.

## Start and finish

1. Read `handoff.md`; inspect branch, recent commits and working-tree changes.
   Verify inherited claims against the repository and preserve other people's edits.
2. Read the assigned task in `PLAN.md` or GitHub, then relevant acceptance checks.
   On first visit read README and CONTRIBUTING. Do not invent owners or issue IDs.
3. Make the smallest useful change, run relevant checks, inspect the diff and update
   affected docs. Update `handoff.md` before ending every session or switching models/agents.

## Current scope and authorization

- The owner-authorized local/hosted baseline is implemented in PRs #22/#24.
  Assignment 3 is a structural reference only; do not copy its code or data.
- Further app development and deployment are paused pending owner/team direction.
  The November 9 documentation task authorizes documentation commit/push only;
  it does not resume app development.
- Initial repository creation, publication, setup commits, CI configuration and
  invitations for the five named collaborators are authorized by the owner.
  Subsequent work follows the user's authorization for that task; do not treat
  this setup authorization as permanent permission to publish unrelated changes.
- Preferred branches: `codex/<task>`. Main is protected by active ruleset 26916067:
  PR, one eligible approval, fresh/latest-push approval, resolved conversations,
  up-to-date branch and passing GitHub Actions `test`. Force pushes and deletion
  are blocked; no actors, including admins, have bypass exemptions.
- The owner's November 9 activation supersedes the earlier disabled-protection
  instruction. Never weaken or bypass these gates. CODEOWNERS remains deferred
  until the team joins. See [current settings](docs/GITHUB_SETUP.md); verify live
  GitHub state before consequential actions. No local blocking hooks are installed.

## Creator and reviewer responsibilities

- Creator: understand acceptance, coordinate shared contracts, implement within
  scope, run relevant checks, inspect safe files and document remaining gaps.
- Reviewer: independently assess correctness, security, acceptance and the user
  flow; give reproduction and expected behavior for a blocking finding.
- An eligible teammate with no PR implementation is the intended human reviewer.
  Joshua also authorized the dedicated Hermes/JoshKozy automated role described
  in CONTRIBUTING; it is not another human. A coding agent cannot switch accounts
  to claim that role. GitHub enforces another reviewing account, not another human.
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
