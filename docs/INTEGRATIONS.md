# Integration status

One Python app and `uv.lock` support local SQLite and hosted Neon PostgreSQL.
The free Render service is <https://operations-tracking-mbax6418.onrender.com>.
PRs #22/#24 established the complete manual-job/report/AI baseline. Hosted desktop
and 390px mobile-sized flows, sign-in/conflict recovery and real course-model drafts
worked against Neon. Records survived redeployment and access after 15+ idle minutes.
[Current deployed commit and package evidence](https://github.com/JoshuaKosakowsky/Operations-Tracking-Application/issues/23)
distinguishes actual hosted checks, synthetic failures and owner feedback.
Local records do not automatically synchronize with the shared database.

The course text service uses port 9001, model
`cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit`, and OpenAI-compatible chat completions with
`chat_template_kwargs.enable_thinking=false`. A bounded real request verified
this contract; local app draft calls provide separate integration evidence.
Port 9000 is reserved exclusively for Hermes. No other model service is needed.

AI inputs are selected saved fields, never browser-supplied prompts. Customer drafts
exclude internal notes; daily drafts include notes and calculated totals. Responses
are bounded, treated as plain text and discarded if source records changed during
generation. Human review is still required: these checks cannot guarantee factual
accuracy. No model tools, record writes, automatic sends, retries or background calls.
Team limits persist in the database: 3 attempts/minute and 20/day, resetting at UTC
window boundaries. Daily input is bounded to 20 jobs and 24 KB; output to 650 tokens.

The course endpoint is HTTP, so both authentication and submitted records lack
transport encryption on that leg. Use fictional records only. Secrets remain in
Render's environment settings or ignored local `.env`. Free hosting does not supply
external AI credits or guarantee the availability of the shared course endpoint.

Google Calendar, Maps and Bouncie remain deferred feasibility investigations in
issues #3 and #6–#8. No credentials, live requests, tracking, route/ETA calculation,
calendar writes or customer messages have been implemented or verified.

Free Render has ephemeral local storage, spins down after 15 idle minutes, and can
take about a minute to wake. Neon provides durable PostgreSQL with free quotas,
idle compute suspension and limited restore history; it is not a long-term backup.
Both services are in Ohio. Automatic app deployment is off; `render.yaml` captures
the reproducible settings. Export important records before reaching account quotas.

References checked November 9, 2026:
- [Render free-service limits](https://render.com/docs/free)
- [Render FastAPI deployment](https://render.com/docs/deploy-fastapi)
- [Neon plan limits](https://neon.com/docs/introduction/plans)
- [Render environment variables](https://render.com/docs/environment-variables)
- [Course model card](https://huggingface.co/cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit)
- [vLLM server documentation](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/)

Free hosting does not include external AI credits. Secrets belong only in the
host's secret settings or ignored local `.env`, never the GitHub repository.
