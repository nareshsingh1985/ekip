# backend/app/vectorstore/qdrant_client.py

from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    qdrant_url = settings.QDRANT_URL.strip()

    if not qdrant_url or qdrant_url == ":memory:":
        client = QdrantClient(location=":memory:")
    else:
        client = QdrantClient(
            url=qdrant_url,
            api_key=settings.QDRANT_API_KEY or None,
        )

    collections = client.get_collections().collections
    existing = {collection.name for collection in collections}

    if settings.COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    return client
