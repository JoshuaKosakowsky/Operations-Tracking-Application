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
| [ ] Generate useful, grounded GenAI drafts | Customer update and daily manager summary from saved data. Human review required; no tools or external sends. No model access configured; live evidence and output-quality feedback pending. |
| [ ] Provide authenticated hosted and local access | Free Render Python service + durable Neon PostgreSQL selected; accounts not created. Same source and `uv.lock`; verify desktop/mobile, idle wake-up, failure recovery and retention after deployment. |
| [ ] Exercise independent clean installation | Automated fresh-ZIP rehearsal is separate. No second person available; invite acceptance and tester/check-in remain unclaimed. |
| [ ] Deliver matching hosted build and source package | Display exact commit; freeze optional features December 8 at 11:59 p.m. Mountain, 48 hours before submission. Verify fresh final ZIP and host at that commit. |
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

- **Codex for Joshua — underway:** implement and coordinate the first job/report
  flow, then AI/hosting. First check-in delivered via local demo; next check-in is
  CI and dedicated reviewer findings on the focused PR.
- **Joshua — first owner test completed:** found the core flow clear. Feedback on
  later AI/hosted integrations must be collected separately.
- **Independent tester / other contributors — unclaimed:** no accepted availability
  or check-in. Assignment alone must not be reported as work underway.
- **Live AI / hosted URL — blocked:** owner confirmed no model access or hosting
  accounts configured. Do not turn synthetic tests into live-service evidence.

[Scope #14](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/14)
and [integrated demo #18](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/18)
track this build. [Project](https://github.com/users/JoshuaKosakowsky/projects/2)
owns live task states. Milestone targets remain Nov 16 / Nov 30 / Dec 10; the first
two are internal targets. Governance #2 remains deferred; safeguards stay disabled.
