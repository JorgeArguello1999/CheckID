from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import face_detection
import face_detection
import google_storage

app = FastAPI()

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
        # Guardando las imagenes en el google cloud
        filename = google_storage.save(images)

        # Realizar la comparación de caras
        answer = face_detection.face_compare(
            filename[0],
            filename[1]
        )

        # Enviando respuesta
        return {
            "euclidean_distance": answer["distance"],
            "answer": answer["answer"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
