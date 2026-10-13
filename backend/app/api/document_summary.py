from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag_service import ask_question

router = APIRouter()


class SummaryRequest(BaseModel):
    filename: str


@router.post("/documents/summary")
def generate_summary(
    req: SummaryRequest
):

    question = (
        f"Provide a concise summary "
        f"of the document "
        f"{req.filename}"
    )

    result = ask_question(question)

    return result