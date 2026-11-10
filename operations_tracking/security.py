"""Team access and persistent, atomic request limits."""

import hashlib
import hmac
import time

from fastapi import HTTPException, Request
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from starlette.responses import JSONResponse

from .store import limits, sessions

COOKIE = "ota_session"


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def consume(engine, name, maximum, seconds):
    now = time.time()
    window = int(now // seconds)
    bucket = f"{name}:{window}"
    insert = sqlite_insert if engine.dialect.name == "sqlite" else pg_insert
    statement = insert(limits).values(bucket=bucket, count=1, expires=(window + 1) * seconds)
    statement = statement.on_conflict_do_update(
        index_elements=[limits.c.bucket], set_={"count": limits.c.count + 1},
        where=limits.c.count < maximum,
    ).returning(limits.c.count)
    with engine.begin() as connection:
        connection.execute(delete(limits).where(limits.c.expires < now))
        allowed = connection.execute(statement).scalar_one_or_none()
    if allowed is None:
        raise HTTPException(429, "Request limit reached. Try again after the current window.",
                            headers={"Retry-After": str(int((window + 1) * seconds - now) + 1)})


def authenticated(request: Request):
    settings = request.app.state.settings
    if not settings.access_code:
        return not settings.production and request.client.host in {"127.0.0.1", "::1"}
    token = request.cookies.get(COOKIE, "")
    if not token or len(token) > 200:
        return False
    with request.app.state.engine.connect() as connection:
        session = connection.execute(select(sessions).where(
            sessions.c.token_hash == digest(token), sessions.c.expires > time.time(),
        )).mappings().first()
    return bool(session and hmac.compare_digest(session["code_hash"], digest(settings.access_code)))


def require_access(request: Request):
    if not authenticated(request):
        raise HTTPException(401, "Enter the team access code to continue.")


class BoundRequestSize:
    """Reject streamed or declared oversized bodies before application parsing."""

    def __init__(self, app, maximum=16384):
        self.app, self.maximum = app, maximum

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] in {"GET", "HEAD"}:
            return await self.app(scope, receive, send)
        chunks, size = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > self.maximum:
                return await JSONResponse({"detail": "Request is too large."}, 413)(scope, receive, send)
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        delivered = False

        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": b"".join(chunks), "more_body": False}
            return await receive()

        await self.app(scope, replay, send)
