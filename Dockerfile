# Use una imagen base de Python
FROM python:3.11

# Establezca el directorio de trabajo en /app
WORKDIR /app

# Copie el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instale las dependencias de Python
RUN pip install -r requirements.txt

# Copie todos los archivos de tu proyecto al directorio de trabajo
COPY . .

# Exponga el puerto que FastAPI usará (generalmente el puerto 8000)
EXPOSE 8000

# Inicie la aplicación FastAPI cuando se ejecute el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

