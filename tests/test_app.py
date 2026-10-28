from fastapi.testclient import TestClient

from operations_tracking.app import app

client = TestClient(app)


def test_health_is_local_and_contains_no_configuration(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-secret-that-must-not-be-returned")
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok", "application": "Operations Tracking Application", "stage": "skeleton",
    }
    assert "test-only-secret" not in response.text


def test_home_and_script_are_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Operations Tracking Application</title>" in response.text
    assert client.get("/assets/status.js").status_code == 200


def test_static_mount_cannot_read_outside_assets():
    assert client.get("/assets/%2e%2e/app.py").status_code == 404


def test_unimplemented_features_are_not_advertised():
    paths = client.get("/openapi.json").json()["paths"]
    assert set(paths) == {"/api/health"}
