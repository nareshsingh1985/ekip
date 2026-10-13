from fastapi import APIRouter

from app.rag.insights_service import (
    generate_executive_summary,
    generate_risks,
    generate_actions,
)

router = APIRouter()

@router.get("/insights/summary")
def executive_summary():

    return {
        "result": generate_executive_summary()
    }

@router.get("/insights/risks")
def risks():
    return {
        "result": generate_risks()
    }

@router.get("/insights/actions")
def actions():

    return {
        "result": generate_actions()
    }