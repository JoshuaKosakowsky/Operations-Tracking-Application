# Hermes reviewer setup and verification

Joshua's Windows installation has a dedicated `operations-reviewer` profile for
`JoshuaKosakowsky/Operations-Tracking-Application`. Its posting identity is
**JoshKozy**; both JoshKozy and JoshuaKosakowsky belong to Joshua. This profile
is separate from the default Hermes agent and the Jukebox reviewer.

The [reviewer policy](HERMES_REVIEWER.md) defines its role. Cloning this repository
does not install the broker, create a profile, grant access or start an agent.
Classmates should use [team onboarding](TEAM_ONBOARDING.md); their coding agents
retain the contributor role.

## Start the existing Windows installation

From PowerShell on Joshua's configured machine:

```powershell
$reviewRoot = Join-Path $env:USERPROFILE 'Documents\Operations-Tracking-Review'
python (Join-Path $reviewRoot 'start_reviewer.py')
```

Run a read-only setup check without a model request or GitHub write:

```powershell
python (Join-Path $reviewRoot 'start_reviewer.py') --check
```

Use a fresh conversation in this dedicated profile. Give Hermes a real PR number
or ask it to inspect ready PRs. It runs on demand; no review watcher or scheduled
job was installed. Its model is currently gpt-6.1-sol through a separate Hermes
Codex-provider sign-in. This inference login is separate from GitHub access.

## Exposed capabilities

The `operations-review` MCP connection exposes exactly six tools:

| Tool | Purpose |
|---|---|
| identity | Verify JoshKozy and the intended repository access |
| read | Read main, PRs, issues, changes, comments and CI information |
| file | Read repository text at an exact commit |
| comment_review | Post disclosed review findings and optional inline comments |
| submit_review | Submit eligible APPROVE or REQUEST_CHANGES verdicts |
| merge_pr | Merge an approved, checked, current PR head into main |

The profile has no terminal, file editor, general API, code runner, commit/push,
patch application, conflict resolution, administration or scheduling tools.
Suggestions describe the expected fix in prose; a separate author implements it.
The role is static review plus platform CI inspection, with no local PR-code,
browser or live-provider execution. It cannot claim another tester's work as its own.

## Connection and merge boundaries

A trusted local broker selects the existing JoshKozy OS-keyring login explicitly
and verifies the actor. Credentials are not returned to the reviewer model.
The underlying GitHub credential can have broader rights than the exposed tools;
this is a restricted tool interface, not an OS sandbox or a merge-only token.
Do not copy local credentials, auth stores or profile state into this repository.

The launcher checks the model-login presence, profile tool restrictions, broker
manifest, GitHub identity and repository Write access. A denied or mismatched
connection stops without falling back to the owner's identity.

Each eligible verdict checks current head/base and role eligibility. Approval
requires passing current CI and no unresolved blocking review, conversation or
author hold. Merge additionally requires JoshKozy's approval of that exact head
and clean mergeability, and preserves existing contributor commits. Writes use a
dry run first. GitHub's merge API pins the head; main is rechecked immediately
before the request because the API has no separate atomic expected-base field.
No protection, review dismissal or conflicting-branch workaround is exposed.

Main's GitHub safeguards are now active under Joshua's later November 9 decision;
[GITHUB_SETUP.md](GITHUB_SETUP.md) records them. Local broker checks supplement
server-side enforcement. Hermes never approves or merges its own policy, tool or
credential changes. Owner authorization does not waive GitHub review/check gates.

## Observed verification - November 9, 2026

- JoshKozy repository Write access and the separate model sign-in were verified.
- Installed broker boundary tests: 14 passed.
- The real Hermes smoke session exposed the six MCP tools and a parallel-call
  wrapper, and called only identity, current-main read and open-PR read.
- That smoke check saw main `87a21bd344c1775dfcc9571879377ca7e49b7469` and zero open PRs.
- The setup smoke posted no review and merged no PR. Subsequently, the dedicated
  profile posted disclosed reviews, requested two fixes on PR #22, verified them,
  and approved/merged eligible PRs #22/#24 after passing checks. Those PR histories
  establish exercised writes; the original smoke and offline tests alone do not.

The installed privileged tooling lives outside this repository. Installation or
repair on another machine is an operator task, not an instruction for Hermes to
expand its own tools. If capabilities fail, report the specific blocker.

## Stop or change the role

Exit the dedicated conversation to stop an active review session. Removing the
profile/connection disables the local tools but does not revoke the underlying
GitHub login. An operator handles credential revocation or access changes.
Changes to the installed profile, broker or policy need owner review; changing
this Markdown alone does not reconfigure a running Hermes session.
