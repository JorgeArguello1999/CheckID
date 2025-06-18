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
        data = {"encode": data}
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

# Check if a DNI is valid
@router.post('/verify_dni/', response_model=v2.APIResponse)
async def verify_dni(
    face_image: UploadFile = File(..., description="Image of the person's face"),
    dni_image: UploadFile = File(..., description="Image of the DNI document"),
    dni_number: str = Form(..., description="10-digit DNI number to verify")
):
    """
    Receives face and DNI images along with a DNI number.
    Validates inputs and delegates the verification process.


    try:
        # Basic input validation
        if not dni_check.validate_dni_format(dni_number):
            raise ValueError("DNI number must be exactly 10 numeric digits")

        allowed_types = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}

        if face_image.content_type not in allowed_types:
            raise ValueError("Face image must be JPEG, PNG or WebP")

        if dni_image.content_type not in allowed_types:
            raise ValueError("DNI image must be JPEG, PNG or WebP")

        # Delegate to the verification service
        verification_result = await dni_check.run_verification(
            face_image=face_image,
            dni_image=dni_image,
            dni_number=dni_number
        )

        return v2.ApiResponseHelper(True, verification_result["message"], verification_result["data"])

    except ValueError as ve:
        return v2.ApiResponseHelper(False, str(ve))

    except Exception as e:
        return v2.ApiResponseHelper(False, f"Internal server error: {str(e)}")
    """