import json

from fastapi.testclient import TestClient

from app.api import upload
from app.main import app
from app import storage

client = TestClient(app)


def test_upload_saves_file_and_metadata(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    metadata_file = tmp_path / "uploads_metadata.json"
    monkeypatch.setattr(upload, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(storage, "METADATA_FILE", metadata_file)
    monkeypatch.setattr(upload, "ingest_document", lambda file_path: None)

    response = client.post(
        "/upload",
        files={"file": ("report.txt", b"upload content", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success", "filename": "report.txt"}
    saved_files = list(upload_dir.iterdir())
    assert len(saved_files) == 1
    assert saved_files[0].read_bytes() == b"upload content"

    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    assert metadata[0]["filename"] == "report.txt"
    assert metadata[0]["file_type"] == ".txt"
    assert metadata[0]["uploaded_at"]


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        "/upload",
        files={"file": ("report.exe", b"content", "application/octet-stream")},
    )

    assert response.status_code == 415
    assert "Supported types" in response.json()["detail"]


def test_upload_removes_file_when_ingestion_fails(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    monkeypatch.setattr(upload, "UPLOAD_DIR", upload_dir)

    def fail_ingestion(file_path):
        raise RuntimeError("ingestion failed")

    monkeypatch.setattr(upload, "ingest_document", fail_ingestion)

    response = client.post(
        "/upload",
        files={"file": ("report.txt", b"upload content", "text/plain")},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "The uploaded file could not be processed. Please try again."
    )
    assert list(upload_dir.iterdir()) == []


def test_upload_history_is_empty_when_metadata_does_not_exist(monkeypatch, tmp_path):
    monkeypatch.setattr(storage, "METADATA_FILE", tmp_path / "missing.json")

    response = client.get("/uploads/history")

    assert response.status_code == 200
    assert response.json() == []
