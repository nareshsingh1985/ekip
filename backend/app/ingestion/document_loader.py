from pathlib import Path

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.docx_loader import load_docx
from app.ingestion.txt_loader import load_txt
from app.ingestion.csv_loader import load_csv
from app.ingestion.excel_loader import load_excel
from app.ingestion.json_loader import load_json

def load_document(file_path: str) -> str:

    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return load_pdf(file_path)

    elif ext == ".docx":
        return load_docx(file_path)

    elif ext == ".txt":
        return load_txt(file_path)

    elif ext == ".csv":
        return load_csv(file_path)

    elif ext in [".xls", ".xlsx"]:
        return load_excel(file_path)

    elif ext == ".json":
        return load_json(file_path)

    raise ValueError(
        f"Unsupported file type: {ext}"
    )