from src import validator, pdf_reader, summarizer
from fastapi import FastAPI, File, UploadFile, HTTPException
import pymupdf

app = FastAPI()

@app.get("/status")
def read_root():
    return {"message": "FastAPI is working"}

@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    try:
        validator.validate(pdf_bytes)
        text = pdf_reader.extract_text(pdf_bytes)
        summary = summarizer.summarize(text)

    except (ValueError, pymupdf.FileDataError) as err: # in case there is an error in the uploaded file
        raise HTTPException(400, f"The uploaded file is invalid!\n {err}")
    
    except summarizer.SummarizationError as summarization_err: # in case the error is on the LLM side
        raise HTTPException(500, f"Some error occured on our end!\n {summarization_err}")

    return {"summary": summary}
