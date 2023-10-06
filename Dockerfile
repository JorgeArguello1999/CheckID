# Use una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN apt-get update 
# Instala gcloud para vertex
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.asc && apt-get update -y && apt-get install google-cloud-sdk -y

# Configura el número de workers como una variable de entorno
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/tokens/validacionbiometrica-2c6740b82cc4.json
ENV GOOGLE_CLOUD_PROJECT="validacionbiometrica"    

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Copia todos los archivos de tu proyecto al directorio de trabajo
COPY . .

# Expon el puerto que FastAPI usará (generalmente el puerto 8000)
EXPOSE 8000

# Inicie la aplicación FastAPI cuando se ejecute el contenedor
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]