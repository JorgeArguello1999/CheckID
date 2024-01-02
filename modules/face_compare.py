from modules.base64_to_numpy import base64_to_numpy
import face_recognition

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