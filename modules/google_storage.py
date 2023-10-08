import os 
from google.cloud import storage
import base64

IMAGEDIR = "./photos/"

def save(cedula_image, faces_image, cedula:str, bucket_name:str):
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
        print(f"Error:    {e}")
        return [filename1, filename2] 