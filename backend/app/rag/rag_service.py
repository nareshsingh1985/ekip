from langchain_core.messages import HumanMessage
from app.llm.openai_client import get_llm
from app.services.search_service import search_documents

def ask_question(question: str):
    results = search_documents(
        question,
        limit = 5
    )

    context = []

    sources = []

    for item in results:
        payload = item.payload

        context.append(
            payload["text"]
        )

        sources.append(
            payload["source"]
        )

    prompt = f"""

You are an enterprise knowledge assistant.

Answer ONLY using the supplied context.

Context:
{' '.join(context)}

Question:
{question}
"""

    llm = get_llm()

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return {
        "answer": response.content,
        "sources": list(set(sources))
    }


def retrieve_context(
    question: str,
    limit: int = 5
):
    results = search_documents(
        question,
        limit
    )

    context = []

    sources = []

    for item in results:
        payload = item.payload

        context.append(
            payload["text"]
        )

        sources.append(
            payload["source"]
        )

    return (
        "\n\n".join(context),
        list(set(sources))
    )
