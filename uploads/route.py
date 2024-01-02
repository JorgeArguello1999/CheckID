from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import BackgroundTasks

from typing import Dict
import json

from uploads.logic import ImageData
from uploads.logic import process_image_data

router = APIRouter()

@router.get("/upload")
async def method_get():
    try:
        # Leemos del `info.json` para mostrar la información
        with open('uploads/info.json', 'r') as file:
            data:dict = json.load(file)
            return data

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

@router.post("/upload")
async def upload_image(data: ImageData, background_tasks: BackgroundTasks):
    result = process_image_data(data)
    return result