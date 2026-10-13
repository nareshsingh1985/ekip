# from langchain_text_splitters import (
#     RecursiveCharacterTextSplitter
# )

# def get_text_splitter():
#     return RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         separators=[
#             "\n\n",
#             "\n",
#             ". ",
#             " ",
#             ""
#             ],
#         length_function=len
#     )

from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        length_function=len
    )