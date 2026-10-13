from app.rag.rag_service import ask_question


def main():
    result = ask_question(
        "What risks are mentioned in the documents?"
    )

    print()
    print(result["answer"])
    print()
    print("Sources:")

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()
