from fastapi import FastAPI, File, UploadFile, Form
from modules import compare_face
from modules import file_handler

import uvicorn

# Start APP
app = FastAPI()

# Clean uploads dirs
print("Cleaning directory")
file_handler.clean_dir()

# View route
@app.get('/')
async def read_root():
    return {
        "name": "CheckID",
        "github": "https://github.com/JorgeArguello1999/CheckID.git",
        "method": "POST",
        "file-type": "only images",

        "compare2faces": {
            "form": {
                "file1": "file1.png",
                "file2": "file2.png",
            },
            "answer": {
                "is_same": "bool",
                "distance": "0-1",
                "encode_faces": [
                    "Encode first photo",
                    "Enconde second photo"
                ]
            }
        },

        "compare1face": {
            "form": {
                "file": "file.png",
                "binary": "encode_image"
            },
            "answer": {
                "distance": "0-1",
                "is_same": "bool"
            }
        },
        
        "get_binary": {
            "form": {
                "file": "file.png",
            }, 
            "answer": "binary file"
        }
    }

# Compare 2 faces 
@app.post('/compare2faces/') 
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

    return {
        "result": result
    }

@app.post('/binary_compare/')
async def binary_compare(file: UploadFile = File(...), binary: str = Form(...)): 
    try:
        file_path = file_handler.save_files([file])
        result = compare_face.compare_binary(file_path[0], binary)
        file_handler.delete_files(file_path)

    except Exception as e:
        result = str(e)
        print(result)
    
    return {
        "result": result
    }

@app.post('/get_binary/')
async def get_binary(file: UploadFile = File(...)):
    try:
        file_path = file_handler.save_files([file])
        result = compare_face.get_binary(file_path[0])
        file_handler.delete_files(file_path)

    except Exception as e:
        result = str(e)
        print(result)
    
    return {
        "result": result
    }

@app.post('/compare_binary/')
async def compare_binary(image: UploadFile = File(...), hex_file: UploadFile = Form(...)):
    try:
        paths = file_handler.save_files([image, hex_file])
        print(paths)
        result = compare_face.files_compares(paths[0], paths[1])
        file_handler.delete_files(paths)
    
    except Exception as e:
        result = str(e)
        print(result)

    return {
        "result": result
    }

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1', 
        port=8000,
        reload=True,
        workers=1
    )