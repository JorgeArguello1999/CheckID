import os 
from google.cloud import storage
import uuid
import base64

GCS_BUCKET_NAME = "imgvalidacion"
IMAGEDIR = "./photos/"

def save(images):
    # Decodificar las imágenes en base64
    image1_data = base64.b64decode(images.image1)
    image2_data = base64.b64decode(images.image2)

    # Generar nombres de archivo únicos
    filename1 = f"{uuid.uuid4()}.jpg"
    filename2 = f"{uuid.uuid4()}.jpg"

    # Guardar las imágenes en el directorio IMAGEDIR
    with open(os.path.join(IMAGEDIR, filename1), "wb") as f1, \
        open(os.path.join(IMAGEDIR, filename2), "wb") as f2:
        f1.write(image1_data)
        f2.write(image2_data)
        
    # Retornando las rutas de guardado 
    filename = [
        os.path.join(IMAGEDIR, filename1),
        os.path.join(IMAGEDIR, filename2)
    ]

    return [filename1, filename2] 

def save_google(images):
    # Decodificar las imágenes en base64
    image1_data = base64.b64decode(images.image1)
    image2_data = base64.b64decode(images.image2)

    # Generar nombres de archivo únicos
    filename1 = f"{uuid.uuid4()}.jpg"
    filename2 = f"{uuid.uuid4()}.jpg"

    # Subir las imágenes a Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    
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