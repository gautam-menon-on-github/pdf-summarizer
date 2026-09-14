from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def read_root():
    return {"message": "FastAPI is working"}
