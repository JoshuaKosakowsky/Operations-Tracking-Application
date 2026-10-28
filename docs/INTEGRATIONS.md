# Planned integrations

Google Calendar and an OpenAI API agent are approved directions for this project.
FastAPI is approved as the server foundation. This milestone implements no provider
clients, OAuth flows, tools, calendar reads/writes or LLM calls; no credentials are needed.

## Decisions required before implementation

| Integration | Decisions still open |
|---|---|
| Google Calendar | User needs, account ownership, read/write operations, narrow OAuth scopes, consent, token storage/refresh/revocation, timezone handling and test account |
| OpenAI | Agent tasks and tools, model, API choice, conversation/data retention, bounded usage/timeouts, cost controls and human authorization for external actions |
| Shared | App authentication, per-user permissions, data model/storage, safe logging, failure recovery and measurable acceptance |

Keep credentials and provider calls on the server; browser code receives only
safe application data. Default startup, health checks and CI must work without
credentials or paid calls. External actions must follow the user's explicit
scope and permissions. Use synthetic fixtures for offline tests; record separately
what live integration checks actually ran.

An OpenAI API integration uses API credentials, distinct from this repository's
GitHub access. Selecting a model or provisioning access is future work. The blank
settings in `.env.example` are placeholders and are not currently consumed.

Official references inspected during setup:

- [OpenAI API authentication and server-side key handling](https://developers.openai.com/api/reference/overview)
- [Google Calendar OAuth scopes](https://developers.google.com/workspace/calendar/api/auth)
- [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

Recheck provider documentation when implementing; these notes are not a frozen API contract.
