import pymupdf

class PDFDataError(Exception):
    pass

def extract_text(pdf_bytes: bytes) -> str:
    """Open the file, read the bytes (PDF only at the moment) and extract the text using pymupdf"""

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)
        
    except Exception as err:
        raise PDFDataError(f"The file cannot be opened: {err}") from err