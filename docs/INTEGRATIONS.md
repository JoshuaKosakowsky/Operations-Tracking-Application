# Integration status

The first app uses manual job input and a local SQLite database. The same schema
supports PostgreSQL for hosting, but no remote database has yet been provisioned
or verified. Shared fields live in `operations_tracking/models.py`.

GenAI is required for final acceptance. The planned first behaviors are a customer
update for one saved job and a manager summary for one day's saved records. Both
are drafts for human review, with no tools, record mutations or external sends.
The owner confirmed no model access is configured. Do not describe disabled
controls, synthetic tests or ordinary arithmetic as a working GenAI integration.

Google Calendar, Maps and Bouncie remain deferred feasibility investigations in
issues #3 and #6–#8. No credentials, live requests, tracking, route/ETA calculation,
calendar writes or customer messages have been implemented or verified.

Hosting choice: free Render Python web service plus free Neon PostgreSQL, avoiding
Render's ephemeral local filesystem and 30-day free database expiry. Account setup
and a live deployment are pending. Provider limits must be rechecked at deployment.

References checked November 9, 2026:
- [Render free-service limits](https://render.com/docs/free)
- [Render FastAPI deployment](https://render.com/docs/deploy-fastapi)
- [Neon plan limits](https://neon.com/docs/introduction/plans)
- [OpenAI text generation](https://developers.openai.com/api/docs/guides/text)

Free hosting does not include external AI credits. Secrets belong only in the
host's secret settings or ignored local `.env`, never the GitHub repository.
