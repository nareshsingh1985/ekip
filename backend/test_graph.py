import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api import graph as graph_api
from app.main import app
from app.services import entity_extraction_service, graph_service

client = TestClient(app)


def test_graph_endpoint_serializes_entity_relationships(monkeypatch):
    def make_graph():
        graph = graph_service.nx.Graph()
        graph.add_node("Project A", group="project")
        graph.add_node("Risk A", group="risk")
        graph.add_edge("Project A", "Risk A", relation="has risk")
        return graph

    monkeypatch.setattr(
        graph_api,
        "build_graph",
        make_graph,
    )

    response = client.get("/graph")

    assert response.status_code == 200
    assert response.json() == {
        "nodes": [
            {"id": "Project A", "label": "Project A", "group": "project"},
            {"id": "Risk A", "label": "Risk A", "group": "risk"},
        ],
        "edges": [
            {"source": "Project A", "target": "Risk A", "label": "has risk"}
        ],
    }


def test_build_graph_adds_only_explicit_relationships(monkeypatch):
    monkeypatch.setattr(
        graph_service,
        "extract_entities",
        lambda: {
            "projects": ["Project A"],
            "risks": ["Risk A"],
            "actions": ["Action A"],
            "teams": [],
            "applications": [],
            "relationships": [
                {
                    "source": "Project A",
                    "target": "Risk A",
                    "relation": "has risk",
                }
            ],
        },
    )

    graph = graph_service.build_graph()

    assert graph.nodes["Project A"]["group"] == "project"
    assert graph.nodes["Risk A"]["group"] == "risk"
    assert graph.nodes["Action A"]["group"] == "action"
    assert list(graph.edges(data=True)) == [
        ("Project A", "Risk A", {"relation": "has risk"})
    ]


def test_entity_extraction_parses_and_normalizes_json(monkeypatch):
    class SearchResult:
        payload = {"text": "Project A has delivery risk Risk A."}

    class LLMResponse:
        content = """```json
        {"projects": [" Project A ", "Project A"], "risks": ["Risk A"],
         "actions": [], "teams": [], "applications": [],
         "relationships": [{"source": "Project A", "target": "Risk A",
                            "relation": "has delivery risk"}]}
        ```"""

    class FakeLLM:
        def invoke(self, prompt):
            return LLMResponse()

    monkeypatch.setattr(
        entity_extraction_service,
        "search_documents",
        lambda query, limit: [SearchResult()],
    )
    monkeypatch.setattr(entity_extraction_service.settings, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(entity_extraction_service, "get_llm", FakeLLM)

    result = entity_extraction_service.extract_entities()

    assert result["projects"] == ["Project A"]
    assert result["risks"] == ["Risk A"]
    assert result["relationships"] == [
        {
            "source": "Project A",
            "target": "Risk A",
            "relation": "has delivery risk",
        }
    ]


def test_entity_extraction_reports_missing_documents(monkeypatch):
    monkeypatch.setattr(
        entity_extraction_service,
        "search_documents",
        lambda query, limit: [],
    )
    monkeypatch.setattr(
        entity_extraction_service,
        "get_llm",
        lambda: pytest.fail("The LLM must not run without indexed documents"),
    )

    with pytest.raises(HTTPException) as error:
        entity_extraction_service.extract_entities()

    assert error.value.status_code == 404


def test_entity_extraction_reports_invalid_model_output(monkeypatch):
    class SearchResult:
        payload = {"text": "Project A has delivery risk Risk A."}

    class LLMResponse:
        content = "This is not JSON"

    class FakeLLM:
        def invoke(self, prompt):
            return LLMResponse()

    monkeypatch.setattr(
        entity_extraction_service,
        "search_documents",
        lambda query, limit: [SearchResult()],
    )
    monkeypatch.setattr(entity_extraction_service.settings, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(entity_extraction_service, "get_llm", FakeLLM)

    with pytest.raises(HTTPException) as error:
        entity_extraction_service.extract_entities()

    assert error.value.status_code == 502
    assert "invalid graph data" in error.value.detail
