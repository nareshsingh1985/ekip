from fastapi import APIRouter

from app.storage import load_upload_metadata

router = APIRouter()

@router.get("/uploads/history")
def upload_history():
    return load_upload_metadata()