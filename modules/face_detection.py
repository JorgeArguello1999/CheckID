from PIL import Image
from io import BytesIO
import numpy as np 
import argparse, base64, face_recognition

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
    # Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
    umbral = 0.5

    # Validamos umbral
    if distancia < umbral:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparar rostros en dos imágenes.")
    parser.add_argument("codigo64_image_1", help="Codigo base64 de la primera imagen.")
    parser.add_argument("codigo64_image_2", help="Código base64 de la primera imagen.")
    parser.add_argument("cedula", help="Número de cédula de la persona.")
    args = parser.parse_args()

    # Leer y codificar la primera imagen en base64
    with open(args.codigo64_image_1, 'rb') as imagen1_file:
        imagen1_base64 = base64.b64encode(imagen1_file.read()).decode('utf-8')

    # Leer y codificar la segunda imagen en base64
    with open(args.codigo64_image_2, 'rb') as imagen2_file:
        imagen2_base64 = base64.b64encode(imagen2_file.read()).decode('utf-8')


    face_compare(imagen1_base64, imagen2_base64, args.cedula)