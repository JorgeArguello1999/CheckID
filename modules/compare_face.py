from face_recognition import face_encodings, compare_faces
from face_recognition import load_image_file
from face_recognition import face_distance

import numpy as np
import pickle
import ast

def encode_image(file) -> np.array:
    """
    Convert file to numpy array
    file: str - Path to the image
    mode: str - Image mode
    return: np.array - For face_recognition
    """
    face = load_image_file(file)
    return face_encodings(face)[0]

def compare_face(image1:str, image2:str) -> dict:
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

    # Distance
    distance = face_distance([face_encoding1], face_encoding2)[0]

    if face_encoding1 is False or face_encoding2 is False:
        return False

    # Compare the faces
    is_same = bool(compare_faces([face_encoding1], face_encoding2, tolerance=0.6)[0]) 

    return {
        "is_same": is_same, 
        "distance": float(distance),
        "encode_faces": [
            str(pickle.dumps(face_encoding1)), 
            str(pickle.dumps(face_encoding2))
        ] 
    }

def compare_binary(image:str, binary:str) -> dict:
    """
    Compare the face vs binary data
    image: str - Image path
    binary: str - All binary from picture
    """
    clean = ast.literal_eval(binary)
    data = pickle.loads(clean)

    # Load image
    image_encode = encode_image(image)

    # Distance 
    distance = face_distance([data], image_encode)[0]

    # Compare the faces
    is_same = bool(compare_faces([data], image_encode, tolerance=0.6)[0])

    return {
        "distance": distance,
        "is_same": is_same
    }

if __name__ == "__main__":
    # compare2faces
    """
    with open("uploads/photo1.png", "rb") as f1, open("uploads/photo1.png", "rb") as f2:
        result = compare_face(f1, f2)
    print(result)
    """

    # compare_binary
    with open('uploads/data.txt', 'r') as data, open('uploads/photo1.png', 'rb') as photo:
        print(data.read())
        result = compare_binary(photo, data.read())
    print(result)