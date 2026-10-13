from app.embeddings.embedding_model import get_embedding_model
from app.vectorstore.qdrant_client import get_qdrant_client
from app.config import settings


def search_documents(
    query: str,
    limit: int = 5
):
    client = get_qdrant_client()
    query_vector = get_embedding_model().encode(
        query
    ).tolist()
    
    results = client.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return results.points