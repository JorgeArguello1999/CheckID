from google.cloud import vision_v1p3beta1 as vision
from google.oauth2 import service_account
import base64, re

def text_detection(credenciales_json:str, image, cedula:str, compare_or_text="compare"):
    """
    Detectar con el OCR de Google el texto de la imagen

    :param credentials -> Ruta donde esta la credencial JSON
    :param image -> Imágen en Base64 
    :param cedula -> Número de cédula en tipo string
    :param compare_or_text -> Elije si comparar las cédulas o solo devolver el texto
    por defecto "compare", en caso contrario escriba "text"
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

        if compare_or_text == "compare":
            return cedula_compare(cedula, texto_completo)
        if compare_or_text == "text":
            return texto_completo
    
    except Exception as e:
        return False

def cedula_compare(cedula:str, img_text:str)-> bool:
    # Filtramos la salida, conservamos solo números
    salida = re.findall(r'\d', img_text)
    salida = (''.join(salida))

    try:
        if cedula in salida:
            print(f"Funciona: {salida}")
            return True 
    except Exception as e:
        print(f"No funciona: {e}")
        return False