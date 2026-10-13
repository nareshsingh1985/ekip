from docx import Document

def load_docx(file_path: str):
    doc = Document(file_path)
    
    return "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )