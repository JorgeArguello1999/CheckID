from fastapi import APIRouter, File, UploadFile, Form
from modules import compare_face, file_handler
from models import v2

import json

router = APIRouter()

# View route
@router.get('/')
async def read_root():
    with open('docs/v2.json', 'r') as file:
        data = json.load(file)
    return data

# Compare 2 faces 
@router.post('/compare2faces/', response_model=v2.APIResponse)
async def upload_file(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    file_paths = []
    try:
        file_paths = file_handler.save_files([file1, file2])

        if len(file_paths) != 2:
            raise ValueError("Invalid files uploaded.")

        data = compare_face.compare_face(file_paths[0], file_paths[1])
        return v2.ApiResponseHelper(True, "Files compared successfully.", data)

    except Exception as e:
        return v2.ApiResponseHelper(False, str(e))

    finally:
        if file_paths: file_handler.delete_files(file_paths)

# Compare face with binary
@router.post('/binary_compare/', response_model=v2.APIResponse)
async def binary_compare(file: UploadFile = File(...), binary: str = Form(...)): 
    file_path = []
    try:
        file_path = file_handler.save_files([file])
        data = compare_face.compare_binary(file_path[0], binary)
        return v2.ApiResponseHelper(True, "Binary comparison successful.", data)

    except Exception as e:
        return v2.ApiResponseHelper(False, str(e))
    
    finally:
        if file_path: file_handler.delete_files(file_path)

# Get binary from image
@router.post('/get_binary/', response_model=v2.APIResponse)
async def get_binary(file: UploadFile = File(...)):
    file_path = []
    try:
        file_path = file_handler.save_files([file])
        data = compare_face.get_binary(file_path[0])
        return v2.ApiResponseHelper(True, "Get binary successful.", data)

    except Exception as e:
        return v2.ApiResponseHelper(False, str(e))
    
    finally: 
        if file_path: file_handler.delete_files(file_path)

# Compare face and hex file
@router.post('/compare_binary/', response_model=v2.APIResponse)
async def compare_binary(image: UploadFile = File(...), hex_file: UploadFile = Form(...)):
    file_paths = []
    try:
        file_paths = file_handler.save_files([image, hex_file])
        data = compare_face.files_compares(file_paths[0], file_paths[1])
        return v2.ApiResponseHelper(True, "Binary compare succesful", data)
    
    except Exception as e:
        return v2.ApiResponseHelper(False, str(e))
    
    finally:
        if file_paths: file_handler.delete_files(file_paths)