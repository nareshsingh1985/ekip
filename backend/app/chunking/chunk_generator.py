from app.chunking.text_splitter import(
    get_text_splitter
)

def create_chunks(text: str):

    splitter = get_text_splitter()

    chunks = splitter.split_text(text)

    return chunks