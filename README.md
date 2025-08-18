# PDF Summary AI

## Overview

**PDF Summary AI** is a simple web application that allows users to upload large PDF documents (up to 50MB, 100 pages) and receive AI-generated summaries using OpenAI's API. The app also keeps a history of the last 5 processed documents.

---

## Features

- **PDF Upload**: Upload PDF files through a web interface.
- **PDF Parsing**: Supports PDFs containing text, images, and tables.
- **Summary Generation**: AI-powered summaries using OpenAI API.
- **History Display**: Shows last 5 uploaded and summarized PDFs.

---

## Project Structure

```
backend/
├── uploads/              # Folder to store uploaded PDF files
├── main.py               # FastAPI application
├── file_validators.py    # File type and pages validations
├── pdf_utils.py          # PDF parsing and preview
├── openai_utils.py       # OpenAI summary generation logic extraction
├── history_utils.py      # Save and retrieve summary history
├── requirements.txt      # Python dependencies

frontend/
├── index.html            # HTML page for uploading PDFs and displaying summaries
├── scripts.js            # Frontend JavaScript logic

.env                      # Environment variables
Dockerfile                # Builds the Django app image
docker-compose.yml        # Defines services
```

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yamarko/pdf-summary-ai.git
cd pdf-summary-ai
```

### 2. Create `.env` file with your configuration:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
CHUNK_MAX_TOKENS=5000
SUMMARY_MAX_TOKENS=200
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Running Locally

#### Backend

```bash
cd backend
uvicorn main:app --reload
```

#### Frontend
Open `frontend/index.html` in your browser.

Or run a simple server:
```bash
cd frontend
py -m http.server 5500
```
Then open your browser at `http://localhost:5500`.

## API Endpoints

### Upload PDF

**POST** `/upload-pdf`

- **Request**: `multipart/form-data` with `file` key.
- **Response**:

```json
{
  "original_filename": "example.pdf",
  "saved_filename": "uuid.pdf",
  "message": "File uploaded successfully",
  "pdf_text_preview": "First 500 chars of PDF...",
  "summary": "AI-generated summary"
}
```

### History

**GET** `/history`

- **Response**: Array of last 5 summaries

```json
[
  {
    "original_filename": "example.pdf",
    "saved_filename": "uuid.pdf",
    "summary": "AI-generated summary"
  }
]
```

## Docker Usage

- `Dockerfile` defines the FastAPI backend environment.
- `docker-compose.yml` maps local `uploads/` folder for persistence.
- `.env` provides environment variables for OpenAI API and token limits.

**Run:**

```bash
docker-compose up --build
```

**Stop:**

```bash
docker-compose down
```

## Notes

- PDF files are limited to 50 MB and 100 pages.
- Partial summaries are generated for large PDFs and combined into a final summary.
- History is stored in `history.json` (ignored in Git).
- CORS is configured to allow frontend JS requests to backend.

