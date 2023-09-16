from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid

app = FastAPI()
IMAGEDIR = "./photos/"

# Welcome message 
@app.get("/")
async def home():
    return {
        "message": "Welcome to Face_Detection API"
    }

# Upload Images
@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}
