# Commit and PR conventions

Use a readable type and imperative subject, for example:

```text
ci: Add clean source archive startup check
```

Types: `feat`, `fix`, `refactor`, `chore`, `perf`, `ci`, `ops`, `build`, `docs`,
`style`, `revert`, `test`. Aim for a short subject without a final period. Explain
non-obvious decisions in the body. Keep each commit focused; wording preferences
are advisory and do not justify unnecessary history rewrites.

Agent branches use `codex/<task>`. PR descriptions lead with the resulting behavior,
link the work item and report actual validation plus remaining gaps. Use `Refs #N`
for partial work and `Closes #N` only when acceptance is met. Before publication,
reference the PLAN milestone ID. Update handoff at session/model transitions.
