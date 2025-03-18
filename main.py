from fastapi import FastAPI, File, UploadFile, Form
from typing import List

import shutil 
import os
import uvicorn

# Start APP
app = FastAPI()

# Upload DIR
updload_dir = 'uploads'
os.makedirs(updload_dir, exist_ok=True)


# View route
@app.get('/')
async def read_root():
    return {
        "name": "CheckID",
        "github": "https://github.com/JorgeArguello1999/CheckID.git",
        "method": "POST",
        "form": {
            "file1": "file1.png",
            "file2": "file2.png",
            "n_id": "123456789"
        }
    }

# Upload route
@app.post('/') 
async def upload_file(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    n_id: str = Form(...),
):

    file_paths = []
    for file in [file1, file2]:
        file_path = os.path.join(updload_dir, file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(file_path)
    
    return {
        "Status": "OK",
        "n_id": n_id,
        "dirs": file_paths
    }


if __name__ == '__main__':
    uvicorn.run(
        app, 
        host='0.0.0.1', 
        port=8000,
        reload=True,
    )