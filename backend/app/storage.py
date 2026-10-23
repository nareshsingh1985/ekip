import json
from pathlib import Path
from typing import Any


BACKEND_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BACKEND_DIR / "uploads"
METADATA_FILE = BACKEND_DIR / "uploads_metadata.json"


def load_upload_metadata() -> list[dict[str, Any]]:
    if not METADATA_FILE.exists():
        return []

    with METADATA_FILE.open("r", encoding="utf-8") as metadata_file:
        metadata = json.load(metadata_file)

    if not isinstance(metadata, list):
        raise ValueError("Upload metadata must be a JSON array")

    return metadata


def save_upload_metadata(metadata: list[dict[str, Any]]) -> None:
    temporary_file = METADATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)
    temporary_file.replace(METADATA_FILE)
