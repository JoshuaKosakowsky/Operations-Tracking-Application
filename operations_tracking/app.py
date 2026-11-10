"""A small, persistent field-crew workday application."""

from contextlib import asynccontextmanager
import csv
from datetime import date, datetime, timezone
import hmac
import io
from pathlib import Path
import secrets
import time
from urllib.parse import urlparse
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, insert, select, update, text
from sqlalchemy.exc import SQLAlchemyError

from . import ai
from .models import JobInput, JobUpdate, Login
from .security import COOKIE, BoundRequestSize, authenticated, consume, digest, require_access
from .settings import Settings
from .store import connect, jobs, metadata, sessions

STATIC = Path(__file__).parent / "static"


def create_app(settings=None, ai_transport=None):
    @asynccontextmanager
    async def lifespan(app):
        app.state.settings = settings or Settings.load()
        app.state.engine = connect(app.state.settings.database_url)
        metadata.create_all(app.state.engine)
        try:
            yield
        finally:
            app.state.engine.dispose()

    app = FastAPI(title="Operations Tracking Application", version="0.2.0", lifespan=lifespan)
    app.add_middleware(BoundRequestSize)
    app.mount("/assets", StaticFiles(directory=STATIC), name="assets")

    @app.middleware("http")
    async def boundary(request, call_next):
        config = request.app.state.settings
        host = urlparse(config.origin).hostname
        if config.production:
            valid_hosts = [host] if host else []
        else:
            valid_hosts = ["localhost", "127.0.0.1", "[::1]", "testserver"]
        # Host checks also protect unauthenticated loopback mode from DNS rebinding.
        hostname = request.headers.get("host", "").split(":")[0]
        if hostname not in valid_hosts:
            return JSONResponse({"detail": "Unrecognized host."}, 400)
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            expected = config.origin if config.production else str(request.base_url).rstrip("/")
            if request.headers.get("x-ota-request") != "1" or (origin and origin != expected):
                return JSONResponse({"detail": "Use this app's controls to submit changes."}, 403)
        response = await call_next(request)
        response.headers.update({
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
        })
        return response

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, error):
        return JSONResponse({"detail": "Storage is unavailable. Your changes were not saved. Retry shortly."}, 503)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, error):
        # Do not reflect submitted values (especially login codes) into error payloads/logs.
        fields = sorted({str(item["loc"][-1]) for item in error.errors()})
        return JSONResponse({"detail": "Check these fields: " + ", ".join(fields)}, 422)

    @app.get("/", include_in_schema=False)
    def home():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/health")
    def health():
        with app.state.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "application": "Operations Tracking Application",
                "stage": "dispatch", "build": app.state.settings.build}

    @app.get("/api/session")
    def session(request: Request):
        return {"authenticated": authenticated(request), "requires_code": bool(app.state.settings.access_code),
                "hosted": app.state.settings.production, "build": app.state.settings.build,
                "timezone": "America/Denver", "ai_available": app.state.settings.ai_available}

    @app.post("/api/login")
    def login(body: Login, response: Response):
        consume(app.state.engine, "login", 30, 900)
        code = app.state.settings.access_code
        if not code or not hmac.compare_digest(body.code.encode(), code.encode()):
            raise HTTPException(401, "Access code not recognized.")
        token = secrets.token_urlsafe(32)
        with app.state.engine.begin() as connection:
            connection.execute(delete(sessions).where(sessions.c.expires < time.time()))
            connection.execute(insert(sessions).values(
                token_hash=digest(token), expires=time.time() + 8 * 3600, code_hash=digest(code),
            ))
        response.set_cookie(COOKIE, token, max_age=8 * 3600, httponly=True,
                            secure=app.state.settings.production, samesite="strict")
        return {"authenticated": True}

    @app.post("/api/logout")
    def logout(request: Request, response: Response):
        with app.state.engine.begin() as connection:
            connection.execute(delete(sessions).where(
                sessions.c.token_hash == digest(request.cookies.get(COOKIE, "")),
            ))
        response.delete_cookie(COOKIE)
        return {"authenticated": False}

    def for_day(day):
        with app.state.engine.connect() as connection:
            return [dict(row) for row in connection.execute(
                select(jobs).where(jobs.c.day == day.isoformat()).order_by(jobs.c.time, jobs.c.title, jobs.c.id)
            ).mappings()]

    def job_values(body):
        return {**body.model_dump(mode="json", exclude={"version"}),
                "updated_at": datetime.now(timezone.utc).isoformat()}

    @app.get("/api/jobs", dependencies=[Depends(require_access)])
    def list_jobs(day: date):
        return {"jobs": for_day(day)}

    @app.post("/api/jobs", status_code=201, dependencies=[Depends(require_access)])
    def create_job(body: JobInput):
        consume(app.state.engine, "write", 120, 60)
        values = {**job_values(body), "id": str(uuid4()), "version": 1}
        with app.state.engine.begin() as connection:
            connection.execute(insert(jobs).values(**values))
        return values

    @app.put("/api/jobs/{job_id}", dependencies=[Depends(require_access)])
    def update_job(job_id: UUID, body: JobUpdate):
        consume(app.state.engine, "write", 120, 60)
        values = {**job_values(body), "version": body.version + 1}
        with app.state.engine.begin() as connection:
            result = connection.execute(update(jobs).where(
                jobs.c.id == str(job_id), jobs.c.version == body.version,
            ).values(**values))
            if not result.rowcount:
                raise HTTPException(409, "This job changed or was removed. Reload it before saving again.")
        return {**values, "id": str(job_id)}

    @app.delete("/api/jobs/{job_id}", dependencies=[Depends(require_access)])
    def delete_job(job_id: UUID, version: int = Query(ge=1)):
        consume(app.state.engine, "write", 120, 60)
        with app.state.engine.begin() as connection:
            result = connection.execute(delete(jobs).where(jobs.c.id == str(job_id), jobs.c.version == version))
            if not result.rowcount:
                raise HTTPException(409, "This job changed or was removed. Refresh before deleting.")
        return {"deleted": True}

    @app.get("/api/report", dependencies=[Depends(require_access)])
    def report(day: date):
        records = for_day(day)
        total = {field: sum(row[field] for row in records)
                 for field in ("travel_minutes", "site_minutes", "miles", "modules")}
        total["miles"] = round(total["miles"], 2)
        total["completed"] = sum(row["status"] == "complete" for row in records)
        total["jobs"] = len(records)
        total["modules_per_site_hour"] = round(total["modules"] / (total["site_minutes"] / 60), 2) if total["site_minutes"] else None
        return {"day": day.isoformat(), "totals": total, "jobs": records,
                "revision": ai.revision(records),
                "basis": "Manually recorded crew time, not individual employee hours or payroll."}

    async def draft(records, kind, reload_records):
        if not app.state.settings.ai_available:
            raise HTTPException(503, "AI is not configured. Job records and reports still work.")
        data = ai.source_data(records, kind)
        # Shared, durable limits bound total team usage, including failed provider attempts.
        consume(app.state.engine, "ai-minute", 3, 60)
        consume(app.state.engine, "ai-day", 20, 86400)
        result = await ai.generate(app.state.settings, data, kind, transport=ai_transport)
        if ai.revision(reload_records()) != ai.revision(records):
            raise HTTPException(409, "The saved records changed while drafting. Refresh and request a new draft.")
        return {"text": result, "day": records[0]["day"], "revision": ai.revision(records),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source": [{"id": row["id"], "version": row["version"]} for row in records]}

    @app.post("/api/drafts/customer/{job_id}", dependencies=[Depends(require_access)])
    async def customer_draft(job_id: UUID, version: int = Query(ge=1)):
        def current():
            with app.state.engine.connect() as connection:
                return [dict(row) for row in connection.execute(select(jobs).where(
                    jobs.c.id == str(job_id))).mappings()]
        records = current()
        if not records or records[0]["version"] != version:
            raise HTTPException(409, "This job changed or was removed. Refresh before requesting a draft.")
        return await draft(records, "customer", current)

    @app.post("/api/drafts/daily", dependencies=[Depends(require_access)])
    async def daily_draft(day: date, revision: str = Query(pattern=r"^[0-9a-f]{64}$")):
        records = for_day(day)
        if ai.revision(records) != revision:
            raise HTTPException(409, "This workday changed. Refresh the report before requesting a draft.")
        return await draft(records, "daily", lambda: for_day(day))

    @app.get("/api/export", dependencies=[Depends(require_access)])
    def export(day: date):
        records = for_day(day)
        fields = [column.name for column in jobs.columns]
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in records:
            writer.writerow({key: ("'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value)
                             for key, value in row.items()})
        return Response(stream.getvalue(), media_type="text/csv",
                        headers={"Content-Disposition": f'attachment; filename="operations-{day}.csv"'})

    return app


app = create_app()
