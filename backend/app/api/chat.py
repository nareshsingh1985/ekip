import json
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag_service import ask_question

router = APIRouter()

CHAT_FILE = "chat_history.json"

if not Path(CHAT_FILE).exists():

    with open(CHAT_FILE, "w") as f:
        json.dump([], f)


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(req: ChatRequest):

    result = ask_question(
        req.question
    )

    with open(CHAT_FILE, "r") as f:

        history = json.load(f)

    history.append(
        {
            "question": req.question,
            "answer": result["answer"]
        }
    )

    with open(CHAT_FILE, "w") as f:

        json.dump(
            history,
            f,
            indent=2
        )

    return result