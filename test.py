import requests
import base64
import time

def calcular_tiempo_ejecucion(funcion):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        print(f"Tiempo de ejecución de '{funcion.__name__}': {tiempo_transcurrido} segundos")
        return resultado
    return wrapper

def stress(): 
    count = 0
    while(True):
        hora_inicio = time.time()
        # Ruta de las imágenes que deseas enviar
        imagen1_path = 'carnet1.jpeg'  # Reemplaza con la ruta de tu primera imagen
        imagen2_path = 'carnet1.jpeg'  # Reemplaza con la ruta de tu segunda imagen

        # Leer y codificar la primera imagen en base64
        with open(imagen1_path, 'rb') as imagen1_file:
            imagen1_base64 = base64.b64encode(imagen1_file.read()).decode('utf-8')

        # Leer y codificar la segunda imagen en base64
        with open(imagen2_path, 'rb') as imagen2_file:
            imagen2_base64 = base64.b64encode(imagen2_file.read()).decode('utf-8')

        # Crear un diccionario con las imágenes codificadas en base64
        data = {
            'image1': imagen1_base64,
            'image2': imagen2_base64
        }

        # URL a la que deseas enviar la solicitud POST
        url = 'http://localhost:8000/upload/'  # Reemplaza con la URL correcta de tu API

        # Configurar la solicitud POST con los datos en formato JSON
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        # Verificar el código de respuesta HTTP
        if response.status_code == 200:
            print("Respuesta del servidor:", response.text)
        else:
            print("La solicitud POST falló con el código de respuesta:", response.status_code)
        
        hora_fin = time.time()
        count = count + 1 
        print(f"Tiempo de respuesta: {(hora_fin - hora_inicio)} Número de petición: {count} ")

if __name__ == "__main__":
    stress()