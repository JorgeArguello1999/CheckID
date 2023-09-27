# Use una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN apt-get update && apt-get install -y tesseract-ocr

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Copia todos los archivos de tu proyecto al directorio de trabajo
COPY . .

# Expon el puerto que FastAPI usará (generalmente el puerto 8000)
EXPOSE 8000

# Inicie la aplicación FastAPI cuando se ejecute el contenedor
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "-w", "4"]