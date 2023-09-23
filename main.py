from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import face_detection
import face_detection
import google_storage

# Start FastAPI
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
        # Comparando las imagenes 
        result = face_detection.face_compare(images.image1, images.image2)
        result["save_on_google"] = False 

        # Guardando las imagenes en el google cloud
        if result["answer"] == True:
            result["save_on_google"] = google_storage.save(images)

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
