from fastapi import APIRouter, File, UploadFile, Form
from modules import compare_face, file_handler
from modules import extract_text
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
    Validates inputs and compares faces.
    """
    file_paths = []

    try: 
        if len(dni_number) != 10 or not dni_number.isdigit():
            return v2.ApiResponseHelper(False, "DNI number must be exactly 10 numeric digits")

        # Save images once
        file_paths = file_handler.save_files([face_image, dni_image])
        if len(file_paths) != 2:
            raise ValueError("Failed to process uploaded files.")

        # Compare faces
        is_same = False
        distance = 0.0
        try: 
            comparison = compare_face.compare_face(
                file_paths[0], file_paths[1], only_result=True
            )
            is_same = comparison['is_same']
            distance = comparison['distance']

        except Exception as e:
            return v2.ApiResponseHelper(False, f"Face comparison failed. Ensure both images are valid. {e}")

        # Verify if the face matches the DNI
        status = False
        try:
            text = extract_text.extract_text_from_image(file_paths[1])
            numbers = extract_text.extract_numbers_from_text(text)
            if dni_number in numbers:
                stauts = True 

        except Exception as e:
            return v2.ApiResponseHelper(False, f"Error verifying DNI: {str(e)}")

        # Message 
        message = "DNI failed verification" 
        if is_same and status:
            message = "DNI verified successfully."

        return v2.ApiResponseHelper(True, message, {
            "face_comparison": {"is_same": is_same, "distance": distance},
            "dni_number": dni_number,
            "dni_status": status
        })


    except Exception as e:
        return v2.ApiResponseHelper(False, f"Error: {str(e)}")

    finally:
        if file_paths:
            try:
                file_handler.delete_files(file_paths)
            except Exception as cleanup_err:
                print(f"Cleanup error: {cleanup_err}")