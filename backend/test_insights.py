import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.api import insights as insights_api
from app.main import app
from app.rag import insights_service

client = TestClient(app)


@pytest.mark.parametrize(
    ("endpoint", "generator"),
    [
        ("/insights/summary", "generate_executive_summary"),
        ("/insights/risks", "generate_risks"),
        ("/insights/actions", "generate_actions"),
    ],
)
def test_insight_endpoints_return_generated_result(monkeypatch, endpoint, generator):
    monkeypatch.setattr(insights_api, generator, lambda: "Generated insight")

    response = client.get(endpoint)

    assert response.status_code == 200
    assert response.json() == {"result": "Generated insight"}


def test_insights_report_missing_indexed_documents(monkeypatch):
    monkeypatch.setattr(
        insights_service,
        "search_documents",
        lambda query, limit: [],
    )
    monkeypatch.setattr(
        insights_service,
        "_ask_llm",
        lambda prompt: pytest.fail("The LLM should not run without document context"),
    )

    response = client.get("/insights/summary")

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No indexed documents were found. Upload a document before generating insights."
    )


def test_insights_report_missing_openai_key(monkeypatch):
    monkeypatch.setattr(insights_service.settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(
        insights_service,
        "get_llm",
        lambda: pytest.fail("The LLM should not initialize without an API key"),
    )

    with pytest.raises(HTTPException) as error:
        insights_service._ask_llm("test prompt")

    assert error.value.status_code == 503
    assert error.value.detail == "OPENAI_API_KEY is not configured on the backend."


@pytest.mark.parametrize(
    ("generator", "expected_query", "expected_prompt_text"),
    [
        (
            insights_service.generate_executive_summary,
            "executive summary",
            "Write an executive summary",
        ),
        (
            insights_service.generate_risks,
            "risks incidents blockers",
            "Identify risks explicitly supported",
        ),
        (
            insights_service.generate_actions,
            "action items tasks commitments",
            "Extract concrete action items",
        ),
    ],
)
def test_each_insight_uses_relevant_search_and_prompt(
    monkeypatch,
    generator,
    expected_query,
    expected_prompt_text,
):
    captured = {}

    class SearchResult:
        payload = {"text": "Relevant document context"}

    def fake_search(query, limit):
        captured["query"] = query
        return [SearchResult()]

    def fake_llm(prompt):
        captured["prompt"] = prompt
        return "Insight result"

    monkeypatch.setattr(insights_service, "search_documents", fake_search)
    monkeypatch.setattr(insights_service, "_ask_llm", fake_llm)

    assert generator() == "Insight result"
    assert expected_query in captured["query"]
    assert expected_prompt_text in captured["prompt"]
    assert "Relevant document context" in captured["prompt"]


def test_insights_extract_text_from_block_response(monkeypatch):
    class FakeResponse:
        content = [
            {"type": "text", "text": "Risk one"},
            {"type": "image", "data": "ignored"},
            {"type": "text", "text": "Risk two"},
        ]

    class FakeLLM:
        def invoke(self, prompt):
            return FakeResponse()

    monkeypatch.setattr(insights_service.settings, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(insights_service, "get_llm", FakeLLM)

    assert insights_service._ask_llm("test prompt") == "Risk one\nRisk two"
