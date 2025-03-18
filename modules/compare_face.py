from face_recognition import (
    load_image_file,
    face_encodings, 
    compare_faces
)

def compare_face(image1:str, image2:str) -> bool:
    """
    Compare two faces and return True if they are the same person
    Remember to use only png images
    image1: str - Path to the first image
    image2: str - Path to the second
    """

    # Load the images
    image1 = load_image_file(image1)
    image2 = load_image_file(image2)

    # Get the face encodings
    face_encoding1 = face_encodings(image1)[0]
    face_encoding2 = face_encodings(image2)[0]

    # Compare the faces
    return compare_faces([face_encoding1], face_encoding2, tolerance=0.6)[0]

if __name__ == "__main__":
    DIR = "uploads/"
    result = compare_face(f"{DIR}photo1.png", f"{DIR}photo1.png")
    print(result)


