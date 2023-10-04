from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form

# Modules
import modules.face_detection as face_detection
import modules.google_storage as google_storage
import modules.text_detection_google as text_detection_google

# Start FastAPI
app = FastAPI()
credenciales_json = 'tokens/validacionbiometrica-2c6740b82cc4.json'

# Modelo para recibir el JSON 
# con las imágenes codificadas en base64
# Y la cédula
class ImageData(BaseModel):
    image1: str
    image2: str
    cedula: str

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
                "image2": "image_in_base64",
                "cedula": "1601000000"
            }
        },
        "response format": {
            "distance": "This value indicates the similarity between the two faces. When the distance is greater than 0.5, the faces are not the same. A distance less than 0.5 indicates similarity",
            "faces": "True or False",
            "cedula": "True or False",
            "save_on_google": "False but is True returns a name the file on google bucket"
        }
    }

# Endpoint para cargar y comparar imágenes en formato JSON
@app.post("/upload/")
async def create_upload_files(data: ImageData):
    try:
        # Comparando las imagenes 
        result = face_detection.face_compare(
            data.image1, 
            data.image2, 
        )

        # Comparando Cedulas
        salida = text_detection_google.text_detection(
            credenciales_json, 
            data.image1,
            data.cedula
        )
        print(salida)

        result["save_on_google"] = False
        # Guardando las imagenes en el google cloud
        if result["faces"] == True and result["cedula"] == True:
            try:
                result["save_on_google"] = google_storage.save_google(data)
            except Exception as e:
                result["save_on_google"] = google_storage.save(data)
                print(f"Erro:   {e}")
        
        return result

    except Exception as e:
        return {
            "error as ocurred": f"{e}"
        }