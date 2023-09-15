import face_recognition

# Cargar las dos imágenes de rostros que deseas comparar
imagen1 = face_recognition.load_image_file("./photos/carnet3.jpeg")
imagen2 = face_recognition.load_image_file("./photos/imagen_4.jpeg")

# Codificar los rostros en ambas imágenes
codificacion1 = face_recognition.face_encodings(imagen1)[0]  # Suponemos que solo hay un rostro en cada imagen
codificacion2 = face_recognition.face_encodings(imagen2)[0]

# Calcular la distancia euclidiana entre las codificaciones
distancia = face_recognition.face_distance([codificacion1], codificacion2)[0]

print(distancia)
# El valor de distancia es un valor entre 0 y 1, donde 0 indica una similitud perfecta
# Puedes establecer un umbral para decidir si las imágenes son suficientemente similares
umbral = 0.5  # Ajusta el umbral según tus necesidades

if distancia < umbral:
    print("Las imágenes son suficientemente similares.")
else:
    print("Las imágenes no son suficientemente similares.")

