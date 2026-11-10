from dataclasses import replace
import csv
import io

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import select

from operations_tracking.app import create_app
from operations_tracking.security import consume
from operations_tracking.settings import Settings
from operations_tracking.store import sessions

HEADERS = {"X-OTA-Request": "1"}
JOB = {"day": "2026-11-10", "time": "08:00", "title": "Training install", "customer": "Example A",
       "site": "Training site", "crew": "Crew A", "status": "on_site", "travel_minutes": 30,
       "site_minutes": 120, "miles": 12.5, "modules": 10, "notes": "First section complete."}


@pytest.fixture
def settings(tmp_path):
    return Settings("sqlite:///" + (tmp_path / "test.db").as_posix())


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings), client=("127.0.0.1", 50000), headers=HEADERS) as test:
        yield test


def test_workday_create_edit_report_and_restart(client, settings):
    saved = client.post("/api/jobs", json=JOB)
    assert saved.status_code == 201
    job = saved.json()
    result = client.put(f"/api/jobs/{job['id']}", json={**JOB, "status": "complete", "version": 1})
    assert result.status_code == 200
    report = client.get("/api/report", params={"day": JOB["day"]}).json()
    assert report["totals"] == {"travel_minutes": 30, "site_minutes": 120, "miles": 12.5,
                               "modules": 10, "completed": 1, "jobs": 1, "modules_per_site_hour": 5.0}
    with TestClient(create_app(settings), client=("127.0.0.1", 50000)) as restarted:
        assert restarted.get("/api/jobs", params={"day": JOB["day"]}).json()["jobs"][0]["status"] == "complete"


def test_conflict_never_overwrites_newer_work(client):
    job = client.post("/api/jobs", json=JOB).json()
    url = f"/api/jobs/{job['id']}"
    assert client.put(url, json={**JOB, "notes": "new", "version": 1}).status_code == 200
    assert client.put(url, json={**JOB, "notes": "stale", "version": 1}).status_code == 409
    assert client.delete(url + "?version=1").status_code == 409
    assert client.get("/api/jobs?day=2026-11-10").json()["jobs"][0]["notes"] == "new"
    assert client.delete(url + "?version=2").status_code == 200


@pytest.mark.parametrize("change", [{"title": "  "}, {"miles": -1}, {"time": "29:00"},
                                    {"status": "approved"}, {"notes": "x" * 2001}, {"day": "2026-02-30"}])
def test_bad_input_is_not_saved(client, change):
    assert client.post("/api/jobs", json={**JOB, **change}).status_code == 422
    assert client.get("/api/jobs?day=2026-11-10").json() == {"jobs": []}


def test_empty_report_and_date_isolation(client):
    client.post("/api/jobs", json=JOB)
    result = client.get("/api/report?day=2026-11-11").json()
    assert result["jobs"] == []
    assert result["totals"]["modules_per_site_hour"] is None


def test_auth_cookies_logout_and_secrets(settings):
    config = replace(settings, access_code="private-test-team-code-123456")
    with TestClient(create_app(config), client=("127.0.0.1", 50000), headers=HEADERS) as client:
        assert client.get("/api/jobs?day=2026-11-10").status_code == 401
        assert client.post("/api/jobs", json=JOB).status_code == 401
        assert client.post("/api/login", json={"code":"wrong"}).status_code == 401
        response = client.post("/api/login", json={"code":config.access_code})
        assert response.status_code == 200
        assert "HttpOnly" in response.headers["set-cookie"]
        assert "SameSite=strict" in response.headers["set-cookie"]
        assert client.get("/api/jobs?day=2026-11-10").status_code == 200
        for endpoint in ("/api/session", "/api/health"):
            assert config.access_code not in client.get(endpoint).text
        with client.app.state.engine.connect() as connection:
            row = connection.execute(select(sessions)).mappings().one()
            assert row["token_hash"] != client.cookies["ota_session"]
        client.post("/api/logout")
        assert client.get("/api/jobs?day=2026-11-10").status_code == 401


def test_cross_origin_and_missing_header_are_rejected(client):
    assert client.post("/api/jobs", json=JOB, headers={"Origin":"https://attacker.example"}).status_code == 403
    client.headers.pop("X-OTA-Request")
    assert client.post("/api/jobs", json=JOB).status_code == 403


def test_nonlocal_clients_cannot_use_passwordless_mode(settings):
    with TestClient(create_app(settings), client=("203.0.113.1", 50000)) as client:
        assert not client.get("/api/session").json()["authenticated"]


def test_host_and_request_size_limits(client):
    assert client.get("/api/health", headers={"Host":"attacker.example"}).status_code == 400
    assert client.post("/api/login", content="x" * 20000).status_code == 413


def test_request_limit_survives_new_connection(client):
    consume(client.app.state.engine, "test-budget", 1, 3600)
    with pytest.raises(Exception) as caught:
        consume(client.app.state.engine, "test-budget", 1, 3600)
    assert caught.value.status_code == 429


def test_export_escapes_spreadsheet_formulas_and_contains_saved_work(client):
    client.post("/api/jobs", json={**JOB, "title": "=1+1"})
    response = client.get("/api/export?day=2026-11-10")
    row = next(csv.DictReader(io.StringIO(response.text)))
    assert row["title"] == "'=1+1"
    assert row["modules"] == "10"


def test_assets_and_health(client, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-leak")
    assert client.get("/api/health").json()["build"] == "test-build"
    assert "must-not-leak" not in client.get("/api/health").text
    assert "<title>Operations Tracking Application</title>" in client.get("/").text
    assert client.get("/assets/status.js").status_code == 200
    assert client.get("/assets/app.css").status_code == 200
    assert client.get("/assets/%2e%2e/app.py").status_code == 404
