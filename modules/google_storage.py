from google.cloud import storage
from google.cloud import storage

# Configurar la credencial desde un archivo JSON descargado desde GCP
credenciales_json = './tokens/validacionbiometrica-2c6740b82cc4.json'
storage_client = storage.Client.from_service_account_json(credenciales_json)

import base64

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
        bucket = storage_client.bucket('imgvalidacion')
    
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

if __name__ == '__main__':
    import base64
    from PIL import Image

    # Ruta de la imagen que quieres convertir a base64
    path_to_image = 'cedula.jpeg'

    # Abrir la imagen
    with open(path_to_image, 'rb') as file:
        img = Image.open(file)
        img.show()  # Abre la imagen en tu visor de imágenes predeterminado

    # Codificar la imagen a base64
    with open(path_to_image, 'rb') as file:
        image_base64 = base64.b64encode(file.read()).decode('utf-8')

    salida = save(image_base64, image_base64, '1600644353')
    print(salida)