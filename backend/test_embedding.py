import sys
from types import ModuleType

from app.embeddings import embedding_model


def test_embedding_model_uses_valid_public_model_id(monkeypatch):
    calls = []
    sentence_transformers = ModuleType("sentence_transformers")
    sentence_transformers.SentenceTransformer = (
        lambda model_id: calls.append(model_id) or model_id
    )
    monkeypatch.setitem(sys.modules, "sentence_transformers", sentence_transformers)
    embedding_model.get_embedding_model.cache_clear()

    try:
        assert embedding_model.get_embedding_model() == "BAAI/bge-small-en-v1.5"
        assert calls == ["BAAI/bge-small-en-v1.5"]
    finally:
        embedding_model.get_embedding_model.cache_clear()

def main():
    vector = embedding_model.get_embedding_model().encode(
        "This is a test vector"
    )
    print(len(vector))


if __name__ == "__main__":
    main()
