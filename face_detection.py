import face_recognition
import argparse
import threading

# Python Modules
from io import BytesIO
from PIL import Image
import base64
import numpy as np 

# Aquí se almacenan las imagenes codificadas
resultados = []

def base64_to_numpy_and_encode(image):
    # Transformamos de base64 a numpy array
    image_bytes = base64.b64decode(image)
    # Crear un objeto BytesIO a partir de los bytes
    image_io = BytesIO(image_bytes)
    # Abrir la imagen utilizando la biblioteca PIL (Pillow)
    image = Image.open(image_io)
    # Convertir la imagen a una matriz numpy
    image_array = np.array(image)
    salida = face_recognition.face_encodings(image_array)[0]
    resultados.append(salida)
    return salida

def face_compare(image1, image2, core=False):
    """
    Recibe imagenes en Base64
    :image1
    :image2
    :Core -> Habilita o Inhabilita el uso de hilos (Beta)
    """
    if core == True:
        hilo1 = threading.Thread(target=base64_to_numpy_and_encode, args=(image1, ))
        hilo2 = threading.Thread(target=base64_to_numpy_and_encode, args=(image2, ))

        hilo1.start()
        hilo2.start()

        hilo1.join()
        hilo2.join()
        print("Method:    Threads")

    else: 
        # Codificar los rostros en ambas imágenes
        resultados[0] = base64_to_numpy_and_encode(image1)
        resultados[1] = base64_to_numpy_and_encode(image2)
        print("Method:    Lineal")

    # No toques la face_distance porque en la documentación esta así y así
    # lo dejamos :)
    distancia = face_recognition.face_distance([resultados[0]], resultados[1])[0]
 
    # El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
    # Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
    umbral = 0.5

    if distancia < umbral:
        answer = True
    else:
        answer = False

    return {
        "distancia": distancia,
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


    face_compare(imagen1_base64, imagen2_base64, core=True)