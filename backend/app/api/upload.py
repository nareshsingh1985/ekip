import json
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from app.services.ingest_service import ingest_document

router = APIRouter()

UPLOAD_DIR = "uploads"
METADATA_FILE = "uploads_metadata.json"

Path(UPLOAD_DIR).mkdir(exist_ok=True)

if not Path(METADATA_FILE).exists():
    with open(METADATA_FILE, "W") as f:
        json.dump([], f)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = (
        f"{UPLOAD_DIR}/{file.filename}"
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:
        f.write(contents)

    ingest_document(file_path)

    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    metadata.append(
        {
            "filename": file.filename,
            "uploaded at": datetime.now().strftime(
                "%Y-%m-%d- % H:%M:%S"
            ),
            "file_type": Path(
                file.filename
            ).suffix
        }
    )

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

    return{
        "status": "success",
        "filename": file.filename
    }