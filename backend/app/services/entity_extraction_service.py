import json

from app.llm.openai_client import get_llm
from app.services.search_service import (
    search_documents
)


def extract_entities():

    results = search_documents(
        "projects risks actions teams applications",
        limit=20
    )

    context = []

    for item in results:

        context.append(
            item.payload["text"]
        )

    text = "\n".join(context)

    prompt = f"""
Extract entities from the text.

Return JSON ONLY.

Format:

{{
  "projects": [],
  "risks": [],
  "actions": [],
  "teams": [],
  "applications": []
}}

Text:

{text}
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    try:
        return json.loads(
            response.content
        )

    except Exception:
        return {
            "projects": [],
            "risks": [],
            "actions": [],
            "teams": [],
            "applications": []
        }