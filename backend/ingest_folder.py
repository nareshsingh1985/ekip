from pathlib import Path

from app.services.ingest_service import(
    ingest_document
)

UPLOAD_DIR = "uploads"

for file in Path(
    UPLOAD_DIR
).iterdir():
    if file.is_file():
        try:
            ingest_document(
                str(file)
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(e)