from app.ingestion.document_loader import load_document
from app.chunking.chunk_generator import create_chunks

def main():
    file_path = "uploads/sample.pdf"
    text = load_document(file_path)
    chunks = create_chunks(text)
    print("Total Chunks:", len(chunks))

    if chunks:
        print()
        print(chunks[0][:500])


if __name__ == "__main__":
    main()
