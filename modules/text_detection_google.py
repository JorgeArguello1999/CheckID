import requests
import json
import base64

# Define las variables de configuración
API_KEY = "YOUR_API_KEY"
PROJECT_ID = "YOUR_PROJECT_ID"

# Realiza la solicitud a la API de Vision
def get_text_from_image(image_base64) -> json:
    """
    :param image_base64 
    Recibe la imagen en base64 y devuelve un json
    """
    url = "https://vision.googleapis.com/v1/images:annotate"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "requests": [
            {
                "image": {"content": image_base64},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["responses"][0]["textAnnotations"]

if __name__ == "__main__":
    print("Este modulo recibe imagenes en base64")