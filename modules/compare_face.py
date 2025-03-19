from face_recognition import face_encodings, compare_faces
from PIL import Image

import numpy as np
import io

async def encode_image(file, mode="RGB") -> np.array:
    """
    Convert file to numpy array
    file: bytes - From API
    mode: str - Image mode
    return: np.array - For face_recognition
    """

    try: 
        files_bytes = await file.read()
        image = Image.open(io.BytesIO(files_bytes))

    except: # noqa
        image = Image.open(file) 

    if mode: 
        image = image.convert(mode) 
    
    return face_encodings(np.array(image))[0]


async def compare_face(image1:str, image2:str) -> bool:
    """
    Compare two faces and return True if they are the same person
    Remember to use only png images
    image1: str - Path to the first image
    image2: str - Path to the second
    """

    # Load the images
    face_encoding1 = await encode_image(image1)
    face_encoding2 = await encode_image(image2)

    # Compare the faces
    return compare_faces([face_encoding1], face_encoding2, tolerance=0.6)[0]

if __name__ == "__main__":
    with open("uploads/photo1.png", "rb") as f1, open("uploads/photo1.png", "rb") as f2:
        result = compare_face(f1, f2)
    print(result)
