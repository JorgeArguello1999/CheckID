from google.cloud import storage
from dotenv import load_dotenv

import base64
import os 

# Iniciamos las variables de entorno
bucket_name = os.getenv('BUCKET')

def save(cedula_image, faces_image, cedula:str):
    """
    Guardamos las imagenes 
    :param cedula_image -> Foto de la Imagen
    :param faces_image -> Foto del rostro
    :param cedula -> Número de cedula 
    :param bucket_name -> Nombre del bucket donde guardar
    """
    # Decodificar las imágenes en base64
    image1_data = base64.b64decode(cedula_image)
    image2_data = base64.b64decode(faces_image)

    # Generar nombres de archivo únicos
    filename1 = f"{cedula}_cedula.jpg"
    filename2 = f"{cedula}_faces.jpg"

    try:
        # Subir las imágenes a Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
    
        blob1 = bucket.blob(filename1)
        blob2 = bucket.blob(filename2)
    
        blob1.upload_from_string(image1_data, content_type="image/jpeg")
        blob2.upload_from_string(image2_data, content_type="image/jpeg")
    
        # Retornar las rutas de guardado en GCS
        gcs_paths = [
            f"{filename1}",
            f"{filename2}"
        ]
        return gcs_paths

    except Exception as e:
        return f"Error: {e}"