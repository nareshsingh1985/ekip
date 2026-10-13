from app.services.search_service import(
    search_documents
)

def main():
    results = search_documents(
        "What is revenue Growth"
    )

    for item in results:
        print("-" * 50)
        print(item.payload["source"])
        print()
        print(item.payload["text"][:500])


if __name__ == "__main__":
    main()
