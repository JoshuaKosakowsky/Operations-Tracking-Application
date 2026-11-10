import asyncio
from dataclasses import replace
import json

from fastapi import HTTPException
from fastapi.testclient import TestClient
import httpx
import pytest
from sqlalchemy import update

from operations_tracking import ai
from operations_tracking.app import create_app
from operations_tracking.security import consume
from operations_tracking.settings import Settings
from operations_tracking.store import jobs

HEADERS = {"X-OTA-Request": "1"}
JOB = {"day": "2026-11-10", "time": "08:00", "title": "Example installation", "customer": "Example A",
       "site": "Training site", "crew": "Crew A", "status": "on_site", "travel_minutes": 30,
       "site_minutes": 120, "miles": 12.5, "modules": 10, "notes": "Internal: check the final section."}


def completion(text="Ten modules are recorded; the job remains on site.", **changes):
    return {"choices": [{"finish_reason": "stop", "message": {"content": text}, **changes}]}


@pytest.fixture
def config(tmp_path):
    return Settings("sqlite:///" + (tmp_path / "ai.db").as_posix(), ai_base_url="https://model.invalid/v1",
                    ai_model="test-model", ai_api_key="private-provider-key")


def client_for(config, handler):
    return TestClient(create_app(config, ai_transport=httpx.MockTransport(handler)),
                      client=("127.0.0.1", 50000), headers=HEADERS)


def test_real_routes_use_saved_data_without_writes_or_secret_exposure(config):
    calls = []

    def provider(request):
        calls.append(request)
        return httpx.Response(200, json=completion())

    with client_for(config, provider) as client:
        assert client.get("/api/session").json()["ai_available"]
        client.get("/api/health")
        assert not calls
        saved = client.post("/api/jobs", json=JOB).json()
        result = client.post(f"/api/drafts/customer/{saved['id']}?version=1")
        assert result.status_code == 200
        assert result.json()["source"] == [{"id": saved["id"], "version": 1}]
        assert result.json()["text"].startswith("Ten modules")
        payload = json.loads(calls[0].content)
        assert payload["model"] == config.ai_model
        assert payload["max_tokens"] == 650
        assert payload["chat_template_kwargs"] == {"enable_thinking": False}
        assert "tools" not in payload and not payload["stream"]
        assert calls[0].headers["Authorization"] == "Bearer " + config.ai_api_key
        assert "Internal:" not in payload["messages"][1]["content"]
        customer_source = json.loads(payload["messages"][1]["content"])["saved_jobs"][0]
        assert customer_source["scheduled_start_mountain"] == "08:00"
        assert customer_source["recorded_status"] == "on_site"
        assert "time" not in customer_source and customer_source["modules_recorded"] == 10
        assert config.ai_api_key not in result.text
        report = client.get("/api/report?day=" + JOB["day"]).json()
        result = client.post("/api/drafts/daily", params={"day": JOB["day"], "revision": report["revision"]})
        assert result.status_code == 200
        daily = json.loads(json.loads(calls[1].content)["messages"][1]["content"])
        assert daily["totals"]["modules"] == 10 and daily["totals"]["site_minutes"] == 120
        assert daily["saved_jobs"][0]["notes"] == JOB["notes"]
        assert client.get("/api/jobs?day=" + JOB["day"]).json()["jobs"] == [saved]


@pytest.mark.parametrize("response", [
    httpx.Response(401, text="private-provider-key error"),
    httpx.Response(429, text="quota detail"),
    httpx.Response(307, headers={"Location": "https://unexpected.invalid"}),
    httpx.Response(200, json=completion("partial", finish_reason="length")),
    httpx.Response(200, json=completion("", message={"content": None, "reasoning_content": "hidden"})),
    httpx.Response(200, json=completion(message={"content": "text", "tool_calls": [{"function": "send"}]})),
    httpx.Response(200, json={"choices": [{"message": [], "finish_reason": "stop"}]}),
    httpx.Response(200, content=b"x" * 65537),
])
def test_provider_failure_is_bounded_generic_and_not_retried(config, response):
    calls = []

    def provider(request):
        calls.append(request)
        return response

    with client_for(config, provider) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        result = client.post(f"/api/drafts/customer/{saved['id']}?version=1")
        assert result.status_code == 502 and len(calls) == 1
        assert config.ai_api_key not in result.text and "quota detail" not in result.text
        assert client.get("/api/jobs?day=" + JOB["day"]).json()["jobs"] == [saved]


def test_timeout_and_total_deadline(config, monkeypatch):
    async def slow(request):
        await asyncio.sleep(0.1)
        return httpx.Response(200, json=completion())

    monkeypatch.setattr(ai, "DEADLINE_SECONDS", 0.01)
    with client_for(config, slow) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        assert client.post(f"/api/drafts/customer/{saved['id']}?version=1").status_code == 504


def test_auth_stale_snapshot_and_empty_day_do_not_call_model(config):
    calls = []
    config = replace(config, access_code="test-shared-code-with-24-characters")
    with client_for(config, lambda request: calls.append(request)) as client:
        assert client.post("/api/drafts/daily?day=2026-11-10&revision=" + "0" * 64).status_code == 401
        client.post("/api/login", json={"code": config.access_code})
        report = client.get("/api/report?day=" + JOB["day"]).json()
        assert client.post("/api/drafts/daily", params={"day": JOB["day"], "revision": report["revision"]}).status_code == 422
        saved = client.post("/api/jobs", json=JOB).json()
        assert client.post(f"/api/drafts/customer/{saved['id']}?version=2").status_code == 409
        assert client.post("/api/drafts/daily", params={"day": JOB["day"], "revision": report["revision"]}).status_code == 409
        assert not calls


def test_changed_records_during_generation_reject_draft(config):
    def provider(request):
        with client.app.state.engine.begin() as connection:
            connection.execute(update(jobs).values(notes="Updated meanwhile", version=2))
        return httpx.Response(200, json=completion())

    with client_for(config, provider) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        assert client.post(f"/api/drafts/customer/{saved['id']}?version=1").status_code == 409


def test_input_and_persistent_team_limits(config):
    calls = []

    def provider(request):
        calls.append(request)
        return httpx.Response(200, json=completion())

    with client_for(config, provider) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        url = f"/api/drafts/customer/{saved['id']}?version=1"
        for _ in range(3):
            assert client.post(url).status_code == 200
        assert client.post(url).status_code == 429
    with client_for(config, provider) as restarted:
        assert restarted.post(url).status_code == 429
    assert len(calls) == 3


def test_daily_limit_and_input_bounds(config):
    with client_for(config, lambda request: pytest.fail("No provider call allowed")) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        for _ in range(20):
            consume(client.app.state.engine, "ai-day", 20, 86400)
        assert client.post(f"/api/drafts/customer/{saved['id']}?version=1").status_code == 429
        for _ in range(20):
            client.post("/api/jobs", json=JOB)
        report = client.get("/api/report?day=" + JOB["day"]).json()
        assert client.post("/api/drafts/daily", params={"day": JOB["day"], "revision": report["revision"]}).status_code == 422
    with pytest.raises(HTTPException) as error:
        ai.source_data([{**JOB, "notes": "x" * 2000}] * 20, "daily")
    assert error.value.status_code == 422


def test_unconfigured_ai_leaves_records_usable(config):
    with client_for(replace(config, ai_api_key=""), lambda request: pytest.fail("No model")) as client:
        saved = client.post("/api/jobs", json=JOB).json()
        assert client.post(f"/api/drafts/customer/{saved['id']}?version=1").status_code == 503
        assert not client.get("/api/session").json()["ai_available"]


def test_customer_omits_zero_module_metric():
    source = json.loads(ai.source_data([{**JOB, "modules": 0}], "customer"))
    assert "modules_recorded" not in source["saved_jobs"][0]


def test_host_and_model_settings(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    for key in ("APP_ORIGIN", "AI_BASE_URL", "AI_MODEL", "AI_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:unused@localhost/test")
    monkeypatch.setenv("TEAM_ACCESS_CODE", "x" * 32)
    monkeypatch.setenv("RENDER_EXTERNAL_URL", "https://example.onrender.com")
    assert Settings.load().origin == "https://example.onrender.com"
    monkeypatch.setenv("APP_ORIGIN", "https://example.onrender.com/path")
    with pytest.raises(ValueError):
        Settings.load()
    monkeypatch.delenv("APP_ORIGIN")
    monkeypatch.setenv("AI_BASE_URL", "http://dobolyi.com:9000/v1")
    monkeypatch.setenv("AI_MODEL", "test")
    monkeypatch.setenv("AI_API_KEY", "secret")
    with pytest.raises(ValueError):
        Settings.load()
    monkeypatch.setenv("AI_BASE_URL", "http://dobolyi.com:9001/v1")
    assert Settings.load().ai_available
