import os
import uuid
import fitz
import pandas as pd


from fastapi import UploadFile, HTTPException
from app.config import settings
from docx import Document as DocxDocument

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def validate_file_extension(filename: str) -> str:
    _, ext = (os.path.splitext(filename.lower()))
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext

async def save_upload_to_disk(file: UploadFile) -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    unique_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path

def extract_text_from_file(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())
    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_from_pdf(path: str) -> str:
    pages = []
    doc = fitz.open(path)

    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"[Page {i + 1}]\n{text}")

    doc.close()
    return "\n\n".join(pages)


def _extract_from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_from_docx(path: str) -> str:
    doc = DocxDocument(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "[document]"

