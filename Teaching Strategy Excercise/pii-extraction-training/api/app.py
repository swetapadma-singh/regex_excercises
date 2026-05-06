from exercises.level10.ex_20 import process_pdfs
from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PII Extraction API is running"}

@app.post("/extract")
async def extract_pii(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_pdfs([temp_path])
    os.remove(temp_path)

    return result