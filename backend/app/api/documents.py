from fastapi import APIRouter

from app.storage import load_upload_metadata

router = APIRouter()


@router.get("/documents")
def get_documents():
    return load_upload_metadata()