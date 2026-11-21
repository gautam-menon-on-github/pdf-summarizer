from src import validator, pdf_reader, summarizer
from fastapi import FastAPI, File, UploadFile, HTTPException

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

    except pdf_reader.EmptyPDFError:
        raise HTTPException(422, "The uploaded PDF contains no extractable text.")

    except (ValueError, pdf_reader.PDFDataError) as err: # in case there is an error in the uploaded file
        raise HTTPException(400, f"The uploaded file is invalid!\n {err}")
    
    except summarizer.SummarizationError: # in case the error is on the LLM side
        raise HTTPException(500, "Summarization failed due to an internal error. Please try again later.")

    return {"summary": summary}
