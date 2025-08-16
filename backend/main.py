from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4

app = FastAPI()

UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    original_name = file.filename
    ext = Path(original_name).suffix[1:]
    unique_filename = f"{uuid4()}.{ext}"
    file_path = UPLOAD_FOLDER / unique_filename

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return JSONResponse(
        {
            "original_filename": original_name,
            "saved_filename": unique_filename,
            "message": "File uploaded successfully",
        }
    )
