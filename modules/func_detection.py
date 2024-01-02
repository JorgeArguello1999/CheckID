from google.cloud import vision_v1p3beta1 as vision
from google.oauth2 import service_account
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

import numpy as np 
import base64, face_recognition
import os

# Cargamos variables de entorno
load_dotenv()

credenciales_json = os.getenv('CREDENTIALS')

# Transformamos de base64 a numpy array
def base64_to_numpy(image):
    image_bytes = base64.b64decode(image)
    # Crear un objeto BytesIO a partir de los bytes
    image_io = BytesIO(image_bytes)
    # Abrir la imagen utilizando la biblioteca PIL (Pillow)
    image = Image.open(image_io)
    # Convertir la imagen a una matriz numpy y encodear
    img_array = np.array(image)
    return {
        "image_encode": face_recognition.face_encodings(img_array)[0],
    }

# Detección de rostros
def face_compare(cedula_image, faces_image):
    """
    Modulo para comparar rostros
    :param cedula_image -> Imágen de la cédula
    :param faces_image -> Imágen del rostro
    """

    # Codificar los rostros en ambas imágenes
    imagen1 = base64_to_numpy(cedula_image)
    imagen2 = base64_to_numpy(faces_image)

    # Calculamos la distancia
    distancia = face_recognition.face_distance(
        [imagen1["image_encode"]], 
        imagen2["image_encode"]
    )[0]
 
    # El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
    if distancia < 0.5:
        faces = True
    else:
        faces = False
    
    return {
        "distance": distancia,
        "faces": faces,
    }

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