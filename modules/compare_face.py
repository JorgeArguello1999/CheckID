from face_recognition import face_encodings, compare_faces
from face_recognition import load_image_file

import numpy as np

def encode_image(file) -> np.array:
    """
    Convert file to numpy array
    file: str - Path to the image
    mode: str - Image mode
    return: np.array - For face_recognition
    """
    face = load_image_file(file)
    return face_encodings(face)[0]

def compare_face(image1:str, image2:str) -> bool:
    """
    Compare two faces and return True if they are the same person
    Remember to use only png images
    image1: str - Path to the first image
    image2: str - Path to the second
    bool: bool - True if the faces are the same
    """

    # Load the images
    face_encoding1 = encode_image(image1) 
    face_encoding2 = encode_image(image2)

    if face_encoding1 is False or face_encoding2 is False:
        return False

    # Compare the faces
    return bool(compare_faces([face_encoding1], face_encoding2, tolerance=0.6)[0])

if __name__ == "__main__":
    with open("uploads/photo1.png", "rb") as f1, open("uploads/photo1.png", "rb") as f2:
        result = compare_face(f1, f2)
    print(result)
