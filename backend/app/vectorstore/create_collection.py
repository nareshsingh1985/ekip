from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from app.vectorstore.qdrant_client import get_qdrant_client

COLLECTION_NAME = "enterprise_knowledge"

def create_collection():
    client = get_qdrant_client()
    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME in existing:
        print("Collection already exists")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )
    print("Collection created successfully")
