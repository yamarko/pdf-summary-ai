from pathlib import Path
import PyPDF2
from fastapi import UploadFile, HTTPException


MAX_PAGES = 100


def validate_file_type(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


def validate_file_pages(file_path: Path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)

    if num_pages > MAX_PAGES:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400, detail=f"PDF has too many pages (max {MAX_PAGES})"
        )
