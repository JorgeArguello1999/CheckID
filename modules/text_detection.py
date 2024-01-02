from google.cloud import vision_v1p3beta1 as vision
from google.oauth2 import service_account

import os
import base64

from dotenv import load_dotenv
# Cargamos variables de entorno
load_dotenv()
credenciales_json = os.getenv('CREDENTIALS')

# Detección de textos
def text_detection(image, cedula:str):
    """
    Detectar con el OCR de Google el texto de la imagen

    :param credentials -> Ruta donde esta la credencial JSON
    :param image -> Imágen en Base64 
    :param cedula -> Número de cédula en tipo string
    """
    # Crear un cliente de Cloud Vision
    credenciales = service_account.Credentials.from_service_account_file(credenciales_json)
    cliente_vision = vision.ImageAnnotatorClient(credentials=credenciales)
    
    # Cargo la imagen en Base64
    contenido_imagen = base64.b64decode(image)

    try:
        # Crear un objeto de imagen
        imagen = vision.Image(content=contenido_imagen)
        # Realizar la solicitud de detección de texto
        resultado = cliente_vision.text_detection(image=imagen)
        textos_detectados = resultado.text_annotations
        # El primer elemento es el texto completo detectado en la imagen
        texto_completo = textos_detectados[0].description

        if cedula in texto_completo:
            return True
        else:
            return False
    
    except Exception as e:
        return False