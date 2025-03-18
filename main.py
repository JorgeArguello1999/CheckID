from fastapi import FastAPI, File, UploadFile, Form
from modules import save_files
import uvicorn

# Start APP
app = FastAPI()

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

    result = "OK" 
    file_paths = []

    try:
        file_paths = save_files([file1, file2])

    except Exception as e:
        result = f"error: {e}"

    return {
        "Status": result,
        "n_id": n_id,
        "dirs": file_paths
    }


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1', 
        port=8000,
        reload=True,
        workers=1
    )