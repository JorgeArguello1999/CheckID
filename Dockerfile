# Use a Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and any other dependency files into the container
COPY pyproject.toml /app/

# Install cmake and other required build tools (g++, make)
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies from pyproject.toml using poetry
RUN pip install --no-cache-dir uv 
RUN uv sync

# Copy the rest of the source code into the container
COPY . /app/

# Expose the port that the FastAPI server will run on
EXPOSE 8000

# List from pip
RUN pip list

# Run the FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
