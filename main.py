from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form


# Modules
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
async def create_upload_files(images: ImageData, cedula:str=Form(...)):
    try:
        # Comparando las imagenes 
        print(cedula)
        cedula = "1600644353"
        result = face_detection.face_compare(
            images.image1, 
            images.image2, 
            cedula
        )
        result["save_on_google"] = False

        # Guardando las imagenes en el google cloud
        if result["answer"] == True:
            result["save_on_google"] = google_storage.save(images)
        
        return result

    except Exception as e:
        # raise HTTPException(status_code=400, detail=str(e))
        return {
            "error as ocurred"
        }