from fastapi import HTTPException

from app.config import settings
from app.llm.openai_client import get_llm
from app.services.search_service import search_documents


def _get_context(query: str):
    results = search_documents(
        query,
        limit=20
    )

    context = [
        item.payload["text"]
        for item in results
        if item.payload and item.payload.get("text")
    ]

    if not context:
        raise HTTPException(
            status_code=404,
            detail="No indexed documents were found. Upload a document before generating insights.",
        )

    return "\n\n".join(context)


def _ask_llm(prompt: str):
    if not settings.OPENAI_API_KEY.strip():
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured on the backend.",
        )

    llm = get_llm()
    response = llm.invoke(prompt)
    content = response.content

    if isinstance(content, str):
        result = content.strip()
    elif isinstance(content, list):
        result = "\n".join(
            block["text"].strip()
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and isinstance(block.get("text"), str)
            and block["text"].strip()
        )
    else:
        result = ""

    if not result:
        raise HTTPException(
            status_code=502,
            detail="The language model returned an empty insight. Please try again.",
        )

    return result


def generate_executive_summary():
    context = _get_context(
        "executive summary business performance key outcomes priorities challenges decisions"
    )
    prompt = f"""Write an executive summary using only facts in the provided documents.
Cover the main situation, key outcomes, important priorities, and decisions needed.
Use concise paragraphs and bullets where useful. Do not invent missing metrics.

Context:

{context}
"""
    return _ask_llm(prompt)


def generate_risks():
    context = _get_context(
        "business project delivery operational compliance risks incidents blockers"
    )
    prompt = f"""Identify risks explicitly supported by the provided documents.
For each risk, state the risk, its evidence, likely impact, and any documented mitigation.
Do not invent severity, impact, or mitigations. If no risks are supported, say so.
Present the findings as a readable numbered list.

Context:

{context}
"""
    return _ask_llm(prompt)


def generate_actions():
    context = _get_context(
        "action items tasks commitments next steps owners deadlines follow-up"
    )
    prompt = f"""Extract concrete action items and commitments from the provided documents.
For each item, include the action and its owner or due date only when stated.
Do not turn general observations into tasks or invent missing owners or dates.
If no action items are supported, say so. Present the findings as a numbered checklist.

Context:

{context}
"""
    return _ask_llm(prompt)