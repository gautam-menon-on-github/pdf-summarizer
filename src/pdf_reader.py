import pymupdf

def extract_text(pdf_bytes: bytes) -> str:
    """Open the file, read the bytes (PDF only at the moment) and extract the text using pymupdf"""

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    string_contents = []

    for page in doc:
        string_contents.append(page.get_text())

    doc.close()
    return "".join(string_contents)