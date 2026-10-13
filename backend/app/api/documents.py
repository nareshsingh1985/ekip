import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

METADATA_FILE = "uploads_metadata.json"


@router.get("/documents")
def get_documents():

    if not Path(METADATA_FILE).exists():
        return []

    with open(METADATA_FILE, "r") as f:
        return json.load(f)