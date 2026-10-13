import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import search_service

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "EKPI backend running!"}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "EKIP",
        "version": "1.0.0",
    }


def test_search_reports_missing_qdrant_configuration(monkeypatch):
    monkeypatch.setattr(search_service.settings, "QDRANT_URL", "")
    monkeypatch.setattr(
        search_service,
        "get_embedding_model",
        lambda: pytest.fail("Embedding model should not load without Qdrant"),
    )

    with pytest.raises(RuntimeError, match="QDRANT_URL is not configured"):
        search_service.search_documents("test query")
