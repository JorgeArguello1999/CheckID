from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
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
"""
@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}
"""
@app.post("/upload/")
async def create_upload_files(files: list[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        # Guardar el archivo
        with open(f"{IMAGEDIR}/{file.filename}", "wb") as f:
            f.write(contents)

        uploaded_files.append({"filename": file.filename})

    return JSONResponse(content=uploaded_files, media_type="application/json")

