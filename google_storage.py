import os 
import uuid
import base64

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