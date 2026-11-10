# GitHub protections and repository setup

Repository: [JoshuaKosakowsky/Operations-Tracking-Application](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application).
Visibility: public. Default branch: `main`.

## Active settings - November 9, 2026, America/Denver

Joshua authorized the controls below, superseding his earlier instruction to keep
safeguards disabled. [Ruleset 26916067](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/rules/26916067)
is active and targets exactly `refs/heads/main`. No bypass actors are configured,
including administrators. [Governance evidence #2](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2)
records verification and remaining work.

| Control | Enforced setting |
|---|---|
| Pull requests | Required; one eligible approving account other than the author. |
| Review freshness | New reviewable commits dismiss approval; the most recent push needs approval from someone other than its pusher. |
| Review conversations | All must be resolved before merging. |
| CI | Aggregate `test`, specifically from GitHub Actions (integration 15368), must pass. |
| Branch currency | The branch must be up to date before merging. |
| Main history | Force pushes and deletion blocked. |
| Secret scanning / push protection | Both verified enabled; supported secrets can be detected/blocked. |
| Dependency monitoring | Dependency graph and Dependabot vulnerability alerts enabled and verified after reload. |

The existing extra-approval setting for unattributed Copilot PRs remains enabled.
JoshKozy has Write access and is an eligible owner-authorized Hermes reviewer;
both accounts belong to Joshua, so another-account approval does not establish
another human's review. The dedicated reviewer's broker adds eligibility checks
and cannot bypass GitHub's rules. It cannot approve or merge changes to its own
policy, tools or credentials; owner authorization does not remove required review/checks.

## Workflow and verification

Use task branches, relevant checks, eligible review and resolved blocking findings.
If no eligible reviewer is available, leave the PR open. Never lower protection to
meet a deadline. [CONTRIBUTING.md](../CONTRIBUTING.md) describes fix verification,
review dismissal and merge responsibilities.

The saved rules were read back through GitHub's API, and security controls were
verified after reload. PR #25 reports merging blocked; no destructive push or merge
test was attempted. CI has read-only repository permissions, checkout does not
persist credentials, Actions are pinned to commit SHAs, and no provider keys or
live model calls are needed for CI.

## Deferred and unchanged

- CODEOWNERS is explicitly deferred until teammates join and agree ownership.
- The dependency audit remains scheduled and path-filtered. Its individual jobs
  are not required merge statuses; docs-only PRs would otherwise wait for jobs
  that never run. A future stable audit gate needs a separate decision.
- Dependabot alerts are on; automatic security/version-update PRs are not enabled.
- No local main-blocking hooks are installed. They would supplement server rules.
- Confirm teammate access and concrete availability through #15; invitations do
  not establish accepted membership or contribution. No license is selected.

## Historical setup

Initial publication on October 27 had unprotected main, zero rulesets and five
pending Write invitations. [Initial test evidence](TEST_RESULTS.md) and #1 are
dated snapshots, superseded by the active settings above. Task planning and the
current application/deployment evidence live in [PLAN.md](../PLAN.md), #18 and #23.
