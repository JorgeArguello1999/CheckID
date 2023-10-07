# Face Compare

Tener en cuenta las variables de entorno, estas son esenciales para hacer la detección de texto en la imagen al igual que guardarlas
en un bucket de google cloud

```bash
export GOOGLE_APPLICATION_CREDENTIALS="your path for gcloud "
export GOOGLE_CLOUD_PROJECT="your project ID"
```

Ademas tener en cuenta que en la sección del códgo de Python para la detección de texto

```python
# Start FastAPI
app = FastAPI()
credenciales_json = './tokens/validacionbiometrica-2c6740b82cc4.json'
```
