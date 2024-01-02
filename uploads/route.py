from fastapi import APIRouter
from fastapi import HTTPException

from typing import Dict
import json

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
