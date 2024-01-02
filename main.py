"""
# main.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
from typing import List
import modules.func_detection as detection
import modules.google_storage as google_storage

app = FastAPI()
credenciales_json = './tokens/validacionbiometrica-2c6740b82cc4.json'
GCS_BUCKET_NAME = "imgvalidacion"

class ImageData(BaseModel):
    cedula_image: str
    faces_image: str
    cedula: str

@app.post("/upload/")
async def create_upload_files(data: ImageData, background_tasks: BackgroundTasks):
    try:
        # Realizar la comparación de imágenes y cédulas sin hilos
        result_images = detection.face_compare(data.cedula_image, data.faces_image)
        result_cedulas = detection.text_detection(credenciales_json, data.cedula_image, data.cedula)

        # Comprobar los resultados y continuar con la parte de guardar en Google
        if result_images["faces"] and result_cedulas:
            # Guardar las imágenes en el google cloud en un hilo único
            background_tasks.add_task(
                google_storage.save,
                data.cedula_image,
                data.faces_image,
                data.cedula,
                GCS_BUCKET_NAME
            )
            save_on_google = [
                f"{data.cedula}_cedula.jpg", 
                f"{data.cedula}_faces.jpg"
            ]
        else:
            save_on_google = False

        # Construir y retornar la respuesta final
        response = {
            "distance": result_images["distance"],
            "faces": result_images["faces"],
            "cedula": result_cedulas,
            "save_on_google": save_on_google  
        }

        return response

    except Exception as e:
        return {
            "error as occurred": str(e)
        }
"""

from fastapi import FastAPI

from home import router as home_route
from uploads import router as upload_route

app = FastAPI()

app.include_router(upload_route)
app.include_router(home_route)

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)