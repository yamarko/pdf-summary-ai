from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from file_validators import validate_file_type, validate_file_pages
from pdf_utils import extract_text_from_pdf
from openai_utils import generate_summary
from history_utils import save_summary_history, get_summary_history

app = FastAPI()

UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    validate_file_type(file)

    original_name = file.filename
    ext = Path(original_name).suffix[1:]
    unique_filename = f"{uuid4()}.{ext}"
    file_path = UPLOAD_FOLDER / unique_filename

    file_size = 0
    chunk_size = 1024 * 1024

    with open(file_path, "wb") as f:
        while content := await file.read(chunk_size):
            file_size += len(content)
            if file_size > MAX_FILE_SIZE:
                break
            f.write(content)

    if file_size > MAX_FILE_SIZE:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="PDF file too large (max 50 MB)")

    validate_file_pages(file_path)

    pdf_text, preview = extract_text_from_pdf(file_path, preview_chars=500)
    summary = generate_summary(pdf_text)
    save_summary_history(original_name, unique_filename, summary)

    return JSONResponse(
        {
            "original_filename": original_name,
            "saved_filename": unique_filename,
            "message": "File uploaded successfully",
            "pdf_text_preview": preview,
            "summary": summary,
        }
    )


@app.get("/history")
async def history():
    data = get_summary_history()
    return JSONResponse(data)
