# CheckID

![logo](checkid.jpeg)

CheckID is a simple API that compares two faces from different images to verify if they belong to the same person. 🚀 It analyzes an identification image and matches it against another photo for secure identity verification. 🔐 Perfect for authentication and security applications! 💡✨

# Features
- Compare two images to verify facial similarity.
- Obtain facial encoding in binary format.
- Compare an image with a pre-existing binary.
- Easy deployment with Docker or native execution with Python.

## Endpoints
### 1. **Compare two faces**
**URL:** `/compare2faces/`

**Method:** `POST`

**Parameters:**
- `file1` (image) - First image to compare.
- `file2` (image) - Second image to compare.

**Response:**
```json
{
    "result": {
        "is_same": true,
        "distance": 0.25,
        "encode_faces": [
            "ENCODED_DATA_1",
            "ENCODED_DATA_2"
        ]
    }
}
```

---
### 2. **Compare an image with a binary**
**URL:** `/binary_compare/`

**Method:** `POST`

**Parameters:**
- `file` (image) - Image to compare.
- `binary` (string) - Facial encoding in binary.

**Response:**
```json
{
    "result": {
        "is_same": false,
        "distance": 0.48
    }
}
```

---
### 3. **Get binary of an image**
**URL:** `/get_binary/`

**Method:** `POST`

**Parameters:**
- `file` (image) - Image to process.

**Response:**
```json
{
    "result": "ENCODED_BINARY_STRING"
}
```

---

# Deployment options

- [Your own docker image](#your-own-docker-image)
- [Download docker image](#donwload-docker-image)
- [Exec with python](#exec-app-with-python)

## Your own Docker Image 

If you want use Docker container you should use the existing `Dockerfile`
```bash
docker build . -t "CheckID:1.0" 
```

## Donwload docker image

Also you can download Docker image from docker hub, for this method you will need:
```bash
docker pull jorgearguello/checkid:latest 
```
Run
```
docker run -d -p 8000:8000 jorgearguello/checkid:latest
```

## Exec app with python 

Finally if you need to make any modifications you should use the source code:
```bash
# Clone the repository
git clone https://github.com/JorgeArguello1999/CheckID.git

# Open dir
cd CheckID

# Install dependencies 
pip install -r pyproject.toml

# Run app
python main.py
```

## Contributing
If you wish to contribute to the development of CheckID, feel free to send Pull Requests or open issues on [GitHub](https://github.com/JorgeArguello1999/CheckID.git).

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

🚀 **Developed by Jorge Arguello** | [GitHub](https://github.com/JorgeArguello1999/)

---