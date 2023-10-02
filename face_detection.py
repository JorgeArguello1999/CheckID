from PIL import Image
import face_recognition, pytesseract
from io import BytesIO
import numpy as np 
import argparse, base64, re

# Función principal
def face_compare(image1, image2, cedula:str):
    """
    Recibe imagenes en Base64
    :param image1
    :param image2
    """
    # Codificar los rostros en ambas imágenes
    imagen1 = base64_to_numpy(image1)
    imagen2 = base64_to_numpy(image2)

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
        answer = True
    else:
        answer = False
    
    # Validamos la cédula
    ced = ced_compare(
        cedula,
        imagen1["image_text"],
        imagen2["image_text"]
    )

    if answer == True and ced == True:
        answer = True
    elif answer == True and ced == False:
        answer = "Ced Problem"
    elif answer == False and ced == True:
        answer = "Face Problem"
    else:
        answer = False

    return {
        "distance": distancia,
        "answer": answer
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
        "image_text": get_text(image)
    }

# Obtener texto de la imagen 
def get_text(image):
    try:
        texto_image = pytesseract.image_to_string(image)
        salida = re.findall(r'\d', texto_image)
        return  ''.join(salida)
    except Exception as e:
       print(f"Error:    {e}")
       return False

# Comparar cédula
def ced_compare(cedula:str, image1, image2):
    print("1era Foto:", image1)
    print("2da Foto:", image2)

    if cedula in image1 or cedula in image2:
        ced = True
    else:
        ced = False
    return ced

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