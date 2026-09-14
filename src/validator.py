def validate(pdf_bytes: bytes) -> None:
    """
    Validates the PDF before reading and extracting contents. 
    It is done to save time, compute resources, LLM API costs etc.
    """
    if not pdf_bytes:
        raise ValueError("The file is empty!")

    if len(pdf_bytes) > 1024 * 1024 * 10:
        raise ValueError("File size exceeds 10MB!")

    if pdf_bytes[:5] != b"%PDF-":
        raise ValueError("The file isn't a PDF.")
