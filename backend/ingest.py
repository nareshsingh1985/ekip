from app.services.ingest_service import(
    ingest_document
)

file_path = "uploads/sample.pdf"

ingest_document(file_path)