import json

from fastapi import APIRouter

router = APIRouter()

METADATA_FILE = "uploads_metadata.json"

@router.get("/uploads/history")
def upload_history():
    with open(METADATA_FILE, "r") as f:
        data = json.load(f)

    return data