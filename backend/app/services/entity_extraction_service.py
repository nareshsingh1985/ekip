import json
import logging
from typing import Any

from fastapi import HTTPException

from app.config import settings
from app.llm.openai_client import get_llm
from app.services.search_service import search_documents

logger = logging.getLogger(__name__)
ENTITY_GROUPS = ("projects", "risks", "actions", "teams", "applications")


def _response_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and isinstance(block.get("text"), str)
        ).strip()
    return ""


def _parse_entities(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        cleaned = cleaned.removesuffix("```").strip()

    try:
        extracted = json.loads(cleaned)
    except json.JSONDecodeError as error:
        logger.warning("Entity extraction returned invalid JSON")
        raise HTTPException(
            status_code=502,
            detail="The language model returned invalid graph data. Please try again.",
        ) from error

    if not isinstance(extracted, dict):
        raise HTTPException(
            status_code=502,
            detail="The language model returned invalid graph data. Please try again.",
        )

    entities: dict[str, Any] = {}
    for group in ENTITY_GROUPS:
        values = extracted.get(group, [])
        if not isinstance(values, list):
            values = []
        entities[group] = list(
            dict.fromkeys(
                value.strip()
                for value in values
                if isinstance(value, str) and value.strip()
            )
        )

    relationships = extracted.get("relationships", [])
    if not isinstance(relationships, list):
        relationships = []
    entities["relationships"] = [
        {
            "source": item["source"].strip(),
            "target": item["target"].strip(),
            "relation": item.get("relation", "related to").strip()
            if isinstance(item.get("relation", "related to"), str)
            else "related to",
        }
        for item in relationships
        if isinstance(item, dict)
        and isinstance(item.get("source"), str)
        and item["source"].strip()
        and isinstance(item.get("target"), str)
        and item["target"].strip()
    ]
    return entities


def extract_entities() -> dict[str, Any]:
    results = search_documents(
        "projects risks actions teams applications",
        limit=20,
    )

    context = [
        item.payload["text"]
        for item in results
        if item.payload
        and isinstance(item.payload.get("text"), str)
        and item.payload["text"].strip()
    ]

    if not context:
        raise HTTPException(
            status_code=404,
            detail="No indexed documents were found. Upload a document before building the knowledge graph.",
        )

    if not settings.OPENAI_API_KEY.strip():
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured on the backend.",
        )

    prompt = f"""Extract only entities and relationships explicitly supported by the text.
Do not invent connections. Return valid JSON only with this exact structure:
{{
  "projects": [],
  "risks": [],
  "actions": [],
  "teams": [],
  "applications": [],
  "relationships": [
    {{"source": "entity name", "target": "entity name", "relation": "relationship"}}
  ]
}}
Every relationship source and target must exactly match an entity name in one of the
entity lists. Use empty arrays when no supported values exist.

Text:
{chr(10).join(context)}
"""

    response = get_llm().invoke(prompt)
    content = _response_text(response.content)
    if not content:
        raise HTTPException(
            status_code=502,
            detail="The language model returned empty graph data. Please try again.",
        )
    return _parse_entities(content)
