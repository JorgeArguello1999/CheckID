from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uuid
import base64

# Import face_detection
import face_detection

app = FastAPI()
IMAGEDIR = "./photos/"

# Modelo para recibir el JSON con las imágenes codificadas en base64
class ImageData(BaseModel):
    image1: str
    image2: str

# Welcome message 
@app.get("/")
async def home():
    return {
        "message": "Welcome to Face_Detection API",
        "author": "Jorge Arguello al3x_argu",
    }

@app.get("/upload/")
async def help():
    return {
        "message": "Welcome to the face detection API",
        "manual": {
            "method": "To use this API, make a POST request with JSON formatted as follows",
            "format": {
                "image1": "image_in_base64", 
                "image2": "image_in_base64"
            }
        },
        "answer": "The response will contain two keys",
        "response format": {
            "euclidean_distance": "This value indicates the similarity between the two faces. When the distance is greater than 0.5, the faces are not the same. A distance less than 0.5 indicates similarity",
            "answer": "True or False"
        }
    }

# Endpoint para cargar y comparar imágenes en formato JSON
@app.post("/upload/")
async def create_upload_files(images: ImageData):
    try:
        # Decodificar las imágenes en base64
        image1_data = base64.b64decode(images.image1)
        image2_data = base64.b64decode(images.image2)

        # Generar nombres de archivo únicos
        filename1 = f"{uuid.uuid4()}.jpg"
        filename2 = f"{uuid.uuid4()}.jpg"

        # Guardar las imágenes en el directorio IMAGEDIR
        with open(os.path.join(IMAGEDIR, filename1), "wb") as f1, \
             open(os.path.join(IMAGEDIR, filename2), "wb") as f2:
            f1.write(image1_data)
            f2.write(image2_data)

        # Realizar la comparación de caras
        answer = face_detection.face_compare(
            os.path.join(IMAGEDIR, filename1),
            os.path.join(IMAGEDIR, filename2)
        )

        # Eliminar los archivos temporales
        os.remove(os.path.join(IMAGEDIR, filename1))
        os.remove(os.path.join(IMAGEDIR, filename2))

        return {
            "euclidean_distance": answer["distance"],
            "answer": answer["answer"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
