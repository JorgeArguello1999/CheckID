from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Lista para almacenar imágenes en memoria
imagenes_en_memoria = []

# Ruta para cargar una imagen y almacenarla en memoria
@app.post("/uploadimage/")
async def upload_image(file: UploadFile):
    # Lee el contenido de la imagen y guárdalo en la lista de imágenes en memoria
    imagen = await file.read()
    imagenes_en_memoria.append(imagen)
    
    # Devuelve una respuesta indicando que la imagen se ha almacenado en memoria
    return {"mensaje": "Imagen almacenada en memoria"}

# Ruta para obtener una lista de todas las imágenes en memoria
@app.get("/getimages/")
async def get_images():
    return imagenes_en_memoria
