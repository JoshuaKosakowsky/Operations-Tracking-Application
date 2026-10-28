# GitHub setup and deferred enforcement

Repository: [JoshuaKosakowsky/Operations-Tracking-Application](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application).
Visibility: public. Default branch: `main`. Fresh Git history.

## Current approved setup

- Publish the setup and configure type/status labels and issue/PR templates.
- Invite `chha7734-web`, `jovi1214`, `mase7919`, `MSpanny`, `prse4479` with Write
  access. An invitation is not an accepted membership; verify and report each state.
- CI runs with read-only repository permissions. Checkout steps do not persist
  credentials. PRs use `pull_request`, never privileged `pull_request_target`.
- GitHub Actions dependencies are pinned to inspected commit SHAs with version comments.
- Provider credentials are unnecessary for setup CI; do not add them to GitHub.
- Task branches and independent reviews are the preferred practice, but no main
  branch protection, required reviews/checks, CODEOWNERS gate or blocking hooks are active.
- No license is selected. Public repository creation does not choose one.

## Required later: GOVERNANCE-01

Activate only after owner authorization. Review the proposed policy with the team:

1. Require PRs and at least one eligible independent approval; no self-approval.
2. Dismiss stale approvals and require approval of the latest reviewable push.
3. Require successful stable CI context `test` and an up-to-date branch. Decide
   separately how to require security audit without blocking docs-only PRs when
   its path-filtered workflow does not run.
4. Require resolved conversations; apply protection to administrators too.
5. Disable force pushes and protected-branch deletion; define any bypass narrowly.
6. Consider local main-blocking hooks as a supplement to server enforcement.
7. Verify the live GitHub policy/readback and test enforcement with a safe PR.

This checklist is a future requirement, not a claim of current protection. Do not
copy Assignment 3's active protection or hook configuration during setup.
Before activation, define current-head review, reviewer-unavailability and merge
responsibilities in CONTRIBUTING. Deadlines do not justify unresolved unsafe changes.
