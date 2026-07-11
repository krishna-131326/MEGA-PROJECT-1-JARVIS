from fastapi.testclient import TestClient
from jarvis.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "llm" in data
    assert "plugins" in data


def test_ready_check():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_chat_endpoint_plugin():
    response = client.post("/api/chat", json={"message": "news"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    # Depending on key it might be error string or success string
    assert data["source"] == "plugin"
    assert data["plugin_used"] == "news"


def test_chat_endpoint_llm():
    response = client.post("/api/chat", json={"message": "hello jarvis"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["source"] == "llm"
    assert data["plugin_used"] is None
