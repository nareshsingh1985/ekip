import json

from fastapi import APIRouter

router = APIRouter()


@router.get("/chat/history")
def history():

    with open(
        "chat_history.json",
        "r"
    ) as f:

        return json.load(f)