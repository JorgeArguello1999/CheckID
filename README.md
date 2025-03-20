# CheckID

![logo](checkid.jpeg)

CheckID is a simple API that compares two faces from different images to verify if they belong to the same person. 🚀 It analyzes an identification image and matches it against another photo for secure identity verification. 🔐 Perfect for authentication and security applications! 💡✨

# I/O APP

## Input

You must be a POST request from Web, PostMan or Curl with this form:
```bash 
curl \
```

## Output

The output will be this:
```json

```

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