from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form

# Modules
import modules.face_detection as face_detection
import modules.google_storage as google_storage
import modules.text_detection_google as text_detection_google

# Start FastAPI
app = FastAPI()
credenciales_json = './tokens/validacionbiometrica-2c6740b82cc4.json'

# Modelo para recibir el JSON 
# con las imágenes codificadas en base64
# Y la cédula
class ImageData(BaseModel):
    cedula_image: str
    faces_image: str
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
        "message": "Bienvenido a API Face_Compare",
        "manual": {
            "method": "La API utiliza una petición POST con formato JSON",
            "format": {
                "cedula_image": "image_in_base64", 
                "faces_image": "image_in_base64",
                "cedula": "1601000000"
            }
        },
        "response format": {
            "distance": "Mientras más cercana a 0, más similares son los rostros",
            "faces": "True or False",
            "cedula": "True or False",
            "save_on_google > True": [
                "1601000000_cedula.jpg",
                "1601000000_faces.jpg"
            ],
            "save_on_google > False": "False"
        }
    }

# Endpoint para cargar y comparar imágenes en formato JSON
@app.post("/upload/")
async def create_upload_files(data: ImageData):
    try:
        # Comparando las imagenes 
        result = face_detection.face_compare(
            data.cedula_image, 
            data.faces_image, 
        )    
        result["save_on_google"] = False

        # Comparando Cedulas
        cedula = text_detection_google.text_detection(credenciales_json, data.cedula_image, data.cedula)
        result["cedula"] = cedula

        # Guardando las imagenes en el google cloud
        if result["faces"] == True and result["cedula"] == True:
            try:
                result["save_on_google"] = google_storage.save_google(data.cedula_image, data.faces_image, data.cedula)

            except Exception as e:
                result["save_on_google"] = google_storage.save(data.cedula_image, data.faces_image, data.cedula)
                print(f"Error:   {e}")
        
        return result

    except Exception as e:
        return {
            "error as ocurred": f"{e}"
        }