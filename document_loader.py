import requests
import io
from PyPDF2 import PdfReader

def load_document_from_url(url: str) -> str:
    """
    Downloads a document from a URL and extracts its text.
    Supports Google Docs export links (plain text) and PDFs.
    """
    response = requests.get(url)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")

    # If it's a PDF (by content-type or URL)
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    else:
        # Assume plain text
        return response.text
