import requests
import json
import base64

# Define las variables de configuración
API_KEY = ""
PROJECT_ID = "validacionbiometrica"

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
    # return response.json()["responses"][0]["textAnnotations"]
    return response

# Obtiene la imagen en base64
def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode("utf-8")

if __name__ == "__main__":
    # image_path = input("Ingresa la ruta: ")
    image_path = "/home/jorge/Imágenes/Fotos_Prueba/cedulas/cedula_tipo.jpeg"
    image_base64 = get_image_base64(image_path)
    text_annotations = get_text_from_image(image_base64)

    print(text_annotations)
    # Imprime el texto de la imagen
    """
    for text_annotation in text_annotations:
        print(text_annotation["description"])
    """