from app.llm.openai_client import get_llm
from app.services.search_service import search_documents

def _get_context():

    results = search_documents(
        "business report policies incidents project",
        limit=20
    )

    context = []

    for item in results:

        context.append(
            item.payload["text"]
        )

    return "\n\n".join(context)

def _ask_llm(prompt: str):
    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content

def generate_executive_summary():

    context = _get_context()

    prompt = f""""
Generate an executive summary.

Context:

{context}
"""

    return _ask_llm(prompt)

def generate_risks():
    context = _get_context()

    prompt = f"""
Identify all business,
delivery,
operational and compliance risks.

Context:

{context}
"""

    return _ask_llm(prompt)


def generate_actions():
    context = _get_context()

    prompt = f"""
Extract all action items.

Context:

{context}
"""
    return _ask_llm(prompt)