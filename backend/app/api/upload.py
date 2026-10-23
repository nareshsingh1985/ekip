import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.services.ingest_service import ingest_document
from app.storage import UPLOAD_DIR, load_upload_metadata, save_upload_metadata

router = APIRouter()
logger = logging.getLogger(__name__)

SUPPORTED_FILE_TYPES = {".pdf", ".docx", ".txt", ".csv", ".xls", ".xlsx", ".json"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    original_filename = (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    if not original_filename:
        raise HTTPException(status_code=400, detail="A filename is required.")

    file_type = Path(original_filename).suffix.lower()
    if file_type not in SUPPORTED_FILE_TYPES:
        supported_types = ", ".join(sorted(SUPPORTED_FILE_TYPES))
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Supported types: {supported_types}.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / f"{uuid4().hex}{file_type}"
    byte_count = 0

    try:
        with file_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                destination.write(chunk)
                byte_count += len(chunk)

        if byte_count == 0:
            file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        await run_in_threadpool(ingest_document, str(file_path))
        metadata = load_upload_metadata()
        metadata.append(
            {
                "filename": original_filename,
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
                "file_type": file_type,
            }
        )
        save_upload_metadata(metadata)
    except HTTPException:
        raise
    except Exception as error:
        file_path.unlink(missing_ok=True)
        logger.exception("Failed to store or process uploaded file %s", original_filename)
        raise HTTPException(
            status_code=500,
            detail="The uploaded file could not be processed. Please try again.",
        ) from error
    finally:
        await file.close()

    return {"status": "success", "filename": original_filename}