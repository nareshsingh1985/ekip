from fastapi import APIRouter
from pydantic import BaseModel

from app.services.search_service import (
    search_documents
)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search(req: SearchRequest):

    results = search_documents(
        req.query,
        limit=10
    )

    output = []

    for item in results:

        output.append(
        {
            "score": round(
                item.score,
                4
            ),
            "source": item.payload.get(
                "source",
                "Unknown"
            ),
            "text": item.payload.get(
                "text",
                ""
            )[:500]
        }
    )

    return output