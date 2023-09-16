from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uuid
import os

# Import face_detection
import face_detection

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
async def create_upload_files(files: list[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        # Guardar el archivo
        with open(f"{IMAGEDIR}/{file.filename}", "wb") as f:
            f.write(contents)

        uploaded_files.append(file.filename)

    answer = face_detection.face_compare(
        IMAGEDIR + uploaded_files[0], 
        IMAGEDIR + uploaded_files[1]
    )

    for images in uploaded_files:
        os.remove(IMAGEDIR + images)

    return {
        "euclidean distance": answer["distance"],
        "answer": answer["answer"]
    }
