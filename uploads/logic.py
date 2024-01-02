from pydantic import BaseModel
import modules.func_detection as detection
import modules.google_storage as google_storage

credenciales_json = './tokens/validacionbiometrica-2c6740b82cc4.json'
GCS_BUCKET_NAME = "imgvalidacion"

class ImageData(BaseModel):
    cedula_image: str
    faces_image: str
    cedula: str

def process_image_data(data: ImageData):
    try:
        # Realizar la comparación de imágenes y cédulas
        result_images = detection.face_compare(data.cedula_image, data.faces_image)
        result_cedulas = detection.text_detection(credenciales_json, data.cedula_image, data.cedula)

        save_on_google = False

        # Comprobar los resultados y continuar con la parte de guardar en Google
        if result_images["faces"] and result_cedulas:
            # Guardar las imágenes en el google cloud
            google_storage.save(data.cedula_image, data.faces_image, data.cedula, GCS_BUCKET_NAME)
            save_on_google = [
                f"{data.cedula}_cedula.jpg", 
                f"{data.cedula}_faces.jpg"
            ]

        # Construir y retornar la respuesta final
        response = {
            "distance": result_images["distance"],
            "faces": result_images["faces"],
            "cedula": result_cedulas,
            "save_on_google": save_on_google  
        }

        return response

    except Exception as e:
        return {
            "error as occurred": str(e)
        }