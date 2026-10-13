from fastapi import APIRouter

from app.vectorstore.qdrant_client import get_qdrant_client
from app.config import settings

router = APIRouter()

@router.get("/dashboard/stats")
def dashboard_stats():
    try:
        collection_info = get_qdrant_client().get_collection(
            collection_name=settings.COLLECTION_NAME
        )

        return {
            "documents": collection_info.points_count or 0,
            "vectors": collection_info.vectors_count or 0,
            "collection": settings.COLLECTION_NAME,
            "status": collection_info.status.value,
        }
    except Exception:
        return {
            "documents": 0,
            "vectors": 0,
            "collection": settings.COLLECTION_NAME,
            "status": "unavailable",
        }