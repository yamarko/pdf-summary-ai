import fitz


def extract_text_from_pdf(pdf_path: str, preview_chars: int = 500) -> tuple[str, str]:
    text = ""
    preview = ""

    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text() + "\n"
            text += page_text
            if len(preview) < preview_chars:
                remaining = preview_chars - len(preview)
                preview += page_text[:remaining]

    return text, preview + ("..." if len(text) > preview_chars else "")
