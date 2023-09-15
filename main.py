import face_recognition

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

    print(distancia)
    # El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
    # Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
    umbral = 0.5

    if distancia < umbral:
        return True
    else:
        return False

if __name__ == "__main__":
    rutas = [
        input("Ingresa la ruta de la primera imagen: "),
        input("Ingresa la ruta de la segunda imagen: ")
    ]
    face_compare(rutas[0], rutas[1])
