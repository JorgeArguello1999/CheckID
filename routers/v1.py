from fastapi import APIRouter, File, UploadFile, Form
from modules import compare_face, file_handler

import json

router = APIRouter()

# View route
@router.get('/')
async def read_root():
    with open('docs/v1.json', 'r') as file:
        data = json.load(file)
    return data

# Compare 2 faces 
@router.post('/compare2faces/') 
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

    return {"result": result}

# Compare face with binary
@router.post('/binary_compare/')
async def binary_compare(file: UploadFile = File(...), binary: str = Form(...)): 
    try:
        file_path = file_handler.save_files([file])
        result = compare_face.compare_binary(file_path[0], binary)
        file_handler.delete_files(file_path)

    except Exception as e:
        result = str(e)
        print(result)
    
    return {"result": result}

# Get binary from image
@router.post('/get_binary/')
async def get_binary(file: UploadFile = File(...)):
    try:
        file_path = file_handler.save_files([file])
        result = compare_face.get_binary(file_path[0])
        file_handler.delete_files(file_path)

    except Exception as e:
        result = str(e)
        print(result)
    
    return {"result": result}

# Compare face and hex file
@router.post('/compare_binary/')
async def compare_binary(image: UploadFile = File(...), hex_file: UploadFile = Form(...)):
    try:
        paths = file_handler.save_files([image, hex_file])
        print(paths)
        result = compare_face.files_compares(paths[0], paths[1])
        file_handler.delete_files(paths)
    
    except Exception as e:
        result = str(e)
        print(result)

    return {"result": result}
