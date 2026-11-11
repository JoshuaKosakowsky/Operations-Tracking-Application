# Required outcomes and evidence

Scope authorized November 9, 2026: build the smallest complete user-facing GenAI
app from the MBAX 6418 brief and Group F operations-tracking proposal. The separate
MSBC 5680 optimization guidelines in the parent folder are not this course's brief.

First user: a manager coordinating a small field-service/solar crew's day.
Scenario: plan a job, assign a crew, record completed work, inspect daily results,
and review an AI draft to communicate the result without inventing facts.

## Required checklist

| Outcome | Current evidence / remaining acceptance |
|---|---|
| [x] Create, assign, update and persist jobs | Local normal launcher and browser walkthrough; 16 backend cases including restart, stale edits, date isolation and validation. Source branch `codex/dispatch-workflow`. |
| [x] Review a daily report and export recorded work | Local browser: 3 fictional jobs, 2 complete, 16 modules after editing; report and CSV behavior covered by tests. |
| [x] Get first owner feedback | Joshua tried job selection, progress/notes, save and Daily report on November 9: “I tested it; the flow is clear.” This is owner testing, not independent testing. |
| [x] Generate useful GenAI drafts for human review | Both local journeys verified against course port 9001; 33 backend cases plus synthetic browser tests. Joshua tested both and reported “useful and clear” on November 9. This is owner feedback, not a guarantee of model accuracy. Hosted AI verification remains in the hosting checklist. |
| [x] Provide authenticated hosted and local access | [Shared app](https://operations-tracking-mbax6418.onrender.com) on free Render + durable Neon. Desktop/mobile-sized AI flow, sign-in/conflict errors, idle access and redeploy retention verified; [exact evidence and build](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/23). Joshua also tested the hosted flow and reported it works clearly. |
| [ ] Exercise independent clean installation | Automated fresh-ZIP rehearsal is separate. No second person available; invite acceptance and tester/check-in remain unclaimed. |
| [x] Rehearse matching hosted build and source package | Exact-commit GitHub ZIP passed fresh extraction, isolated install, normal launcher, build-ID and save/report checks. [Current build/package evidence](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/23). This is automated rehearsal, not independent human testing. |
| [ ] Freeze and recheck the final submission | Freeze optional features December 8 at 11:59 p.m. Mountain, 48 hours before submission. Repeat final ZIP/host identity and acceptance after any later changes. |
| [ ] Complete course materials | Accessible GitHub link; runnable export/README; PPTX/PDF slides; 10–12 minute MP4 presentation; individual peer evaluations. Final submission December 10, 2026, 11:59 p.m. America/Denver. |

## Scope and interface

Required job fields: ID, workday, scheduled local time, name, customer label, site,
crew, progress, travel minutes, site minutes, miles, modules, notes, version and
UTC update timestamp. Shared API contract is in [models.py](operations_tracking/models.py)
and `/docs`. UI uses only server endpoints; no credentials or provider calls in
browser code. Updates must present the last-read version.

SQLite persists local records; PostgreSQL persists hosted records. One team access
code grants access to the shared workspace. This is a fictional-data classroom
prototype, not employee-level access, payroll, a backup service or live dispatch.

Optional/deferred: Google Calendar sync, Bouncie tracking, Maps routes/verified ETAs,
shift inference, maintenance predictions, automated notifications, payroll and
individual roles. Existing service-feasibility issues remain open. No integration
is represented as connected just because its inputs can be entered manually.

## Claims, check-ins and blockers

- **Codex for Joshua — first complete baseline delivered:** PRs #22/#24 merged
  after CI and dedicated Hermes review; hosted/local journeys and clean ZIP verified.
  Latest tested source and any delivery follow-up are recorded in #18/#23.
- **Joshua — owner tests completed:** found the core flow clear, then separately
  tested both local AI journeys and found the text/review/copy controls useful and clear.
  Joshua subsequently tested the hosted flow and reported it works clearly.
  None of these owner checks substitutes for independent testing.
- **Independent tester / other contributors — unclaimed:** no accepted availability
  or check-in. Assignment alone must not be reported as work underway.
- **Service access — ready:** owner activated Render/Neon accounts, supplied the
  course endpoint and approved the free deployment. The model uses HTTP; only
  fictional records are suitable. Synthetic tests remain separate from live evidence.

[Scope #14](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/14)
and [integrated demo #18](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/18)
track this build. [Project](https://github.com/users/JoshuaKosakowsky/projects/2)
owns live task states. Milestone targets remain Nov 16 / Nov 30 / Dec 10; the first
two are internal targets. [Governance #2](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/2)
records active PR/approval/CI/conversation protections and repository security
settings. CODEOWNERS remains deferred until the team joins; further app development
and deployment await owner/team direction.
