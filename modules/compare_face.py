from face_recognition import face_encodings, compare_faces
from face_recognition import load_image_file
from face_recognition import face_distance

import numpy as np
import pickle

TOLERANCE = 0.6

def encode_image(file) -> np.array:
    """
    Convert file to numpy array
    file: str - Path to the image
    mode: str - Image mode
    return: np.array - For face_recognition
    """
    face = load_image_file(file)
    return face_encodings(face)[0]

def compare_face(image1:str, image2:str, tol:float=TOLERANCE, only_result:bool=False) -> dict:
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

    # Distance
    distance = face_distance([face_encoding1], face_encoding2)[0]

    # Compare the faces
    is_same = bool(distance < tol)

    if only_result:
        return {
            "is_same": is_same, 
            "distance": float(distance)
        }

    return {
        "is_same": is_same, 
        "distance": float(distance),
        "encode_faces": [
            str(pickle.dumps(face_encoding1).hex()), 
            str(pickle.dumps(face_encoding2).hex())
        ] 
    }

def compare_binary(image:str, binary:str, tol:float=TOLERANCE) -> dict:
    """
    Compare the face vs binary data
    image: str - Image path
    binary: str - All binary from picture
    """
    binary = binary.strip("'").strip('"')
    data = bytes.fromhex(binary)
    data = pickle.loads(data)

    # Load image
    image_encode = encode_image(image)

    # Distance 
    distance = face_distance([data], image_encode)[0]

    # Compare the faces
    is_same = bool(distance < tol)

    return {
        "distance": distance,
        "is_same": is_same
    }

def get_binary(image:str) -> str:
    """
    Get binary encode from picture
    image: str - File path
    """

    # Load image
    image_encode = encode_image(image)

    # Encode
    image_encode = pickle.dumps(image_encode).hex()

    return str(image_encode)

def files_compares(imagen: str, hex_file: str, tol:float=TOLERANCE) -> dict:
    try:
        with open(hex_file, 'rb') as file:
            binary_data = file.read()
        
        try:
            data = pickle.loads(bytes.fromhex(binary_data.decode('utf-8').strip("'\"")))
        except Exception as e:
            return {"error": "Didn't load binaries"}
        
        image_encode = encode_image(imagen)
        distance = face_distance([data], image_encode)[0]
        is_same = bool(distance < tol)
        
        return {
            "distance": float(distance),
            "is_same": is_same
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    """
    # compare2faces
    with open("uploads/photo1.png", "rb") as f1, open("uploads/photo1.png", "rb") as f2:
        result = compare_face(f1, f2)
    print(result)

    # compare_binary
    with open('uploads/data.txt', 'r') as data, open('uploads/photo1.png', 'rb') as photo:
        result = compare_binary(photo, data.read())
    print(result)
    """

    # get_binary
    with open('uploads/photo1.png', 'rb') as photo:
        result = get_binary(photo)
    print(result)