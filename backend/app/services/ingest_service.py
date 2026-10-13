from uuid import uuid4

from qdrant_client.models import PointStruct

from app.chunking.chunk_generator import create_chunks
from app.embeddings.embedding_model import get_embedding_model
from app.ingestion.document_loader import load_document
from app.vectorstore.qdrant_client import get_qdrant_client
from app.config import settings


def ingest_document(file_path: str):
    client = get_qdrant_client()

    print(f"Processing...: {file_path}")

    text = load_document(file_path)

    chunks = create_chunks(text)

    points = []

    for chunk in chunks:

        vector = get_embedding_model().encode(
            chunk
        ).tolist()

        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "source": file_path
            }
        )
        points.append(point)

    client.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=points,
        wait=True
    )

    print(
        f"{len(points)} chunk inserted"
    )
