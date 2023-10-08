from PIL import Image
from io import BytesIO
import numpy as np 
import base64, face_recognition

# Función principal
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