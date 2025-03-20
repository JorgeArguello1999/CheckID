from fastapi import FastAPI, File, UploadFile
from modules import compare_face
from modules import file_handler

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
        "file-type": "only images",
        "form": {
            "file1": "file1.png",
            "file2": "file2.png",
        },
        "output": {
            "is_same": "bool",
            "distance": "0-1",
            "encode_faces": [
                "numpy array from the first photo",
                "numpy array from the second photo"
            ]
        }
    }

# Upload route
@app.post('/') 
async def upload_file(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        file_paths = file_handler.save_files([file1, file2])
        if len(file_paths) != 2:
            file_handler.delete_files(file_paths)
            raise Exception("Invalid files")

        result = compare_face.compare_face(file_paths[0], file_paths[1])
        file_handler.delete_files(file_paths)

    except Exception as e:
        print(str(e))
        result = f"error: {e}"

    print(result)
    return {
        "status": result
    }

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1', 
        port=8000,
        reload=True,
        workers=1
    )