from PIL import Image
from io import BytesIO
import face_recognition
import argparse
import base64
import numpy as np 
import pytesseract

# Transformamos de base64 a numpy array
def base64_to_numpy(image):
    image_bytes = base64.b64decode(image)
    # Crear un objeto BytesIO a partir de los bytes
    image_io = BytesIO(image_bytes)
    # Abrir la imagen utilizando la biblioteca PIL (Pillow)
    image = Image.open(image_io)
    # Convertir la imagen a una matriz numpy y encodear
    return [
        face_recognition.face_encodings(np.array(image))[0],
        get_text(image)
    ]

# Obtener texto de la imagen 
def get_text(image):
    try:
        texto_image = pytesseract.image_to_string(image)
        return texto_image 
    except Exception as e:
       print(f"Error:    {e}")
       return False
    
def face_compare(image1, image2, cedula:str):
    """
    Recibe imagenes en Base64
    :image1
    :image2
    :Core -> Habilita o Inhabilita el uso de hilos (Beta)
    """
    # Codificar los rostros en ambas imágenes
    codificacion1 = base64_to_numpy(image1)
    codificacion2 = base64_to_numpy(image2)

    # No toques la face_distance porque en la documentación esta así y así
    # lo dejamos :)
    distancia = face_recognition.face_distance([codificacion1[0]], codificacion2[0])[0]
 
    # El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
    # Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
    umbral = 0.5

    # Validamos umbral
    if distancia < umbral:
        answer = True
    else:
        answer = False

    # Validamos cedulas
    if cedula in codificacion1[1] or cedula in codificacion2[1]:
        ced = True
    else:
        ced = False

    return {
        "distancia": distancia,
        "cedula": ced,
        "answer": answer
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparar rostros en dos imágenes.")
    parser.add_argument("codigo64_image_1", help="Codigo base64 de la primera imagen.")
    parser.add_argument("codigo64_image_2", help="Código base64 de la primera imagen.")
    args = parser.parse_args()

    # Leer y codificar la primera imagen en base64
    with open(args.codigo64_image_1, 'rb') as imagen1_file:
        imagen1_base64 = base64.b64encode(imagen1_file.read()).decode('utf-8')

    # Leer y codificar la segunda imagen en base64
    with open(args.codigo64_image_2, 'rb') as imagen2_file:
        imagen2_base64 = base64.b64encode(imagen2_file.read()).decode('utf-8')


    face_compare(imagen1_base64, imagen2_base64)