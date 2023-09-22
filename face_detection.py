import face_recognition
import argparse

def face_compare(ruta_1, ruta_2):
    # Cargar las dos imágenes de rostros que deseas comparar
    imagen1 = face_recognition.load_image_file(ruta_1)
    imagen2 = face_recognition.load_image_file(ruta_2)

    # Codificar los rostros en ambas imágenes
    # Suponemos que solo hay un rostro en cada imagen
    codificacion1 = face_recognition.face_encodings(imagen1)[0]  
    codificacion2 = face_recognition.face_encodings(imagen2)[0]

    # Calcular la distancia euclidiana entre las codificaciones
    distancia = face_recognition.face_distance([codificacion1], codificacion2)[0]

    # El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
    # Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
    umbral = 0.5

    if distancia < umbral:
        print("Similares")
        return {
            "distance": distancia,
            "answer": True
        }

    else:
        print("No similares")
        return {
            "distance": distancia,
            "answer": False
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparar rostros en dos imágenes.")

    parser.add_argument("ruta_1", help="Ruta de la primera imagen.")
    parser.add_argument("ruta_2", help="Ruta de la segunda imagen.")

    args = parser.parse_args()

    face_compare(args.ruta_1, args.ruta_2)