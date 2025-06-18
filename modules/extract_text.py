from google.cloud import vision
import io

from dotenv import load_dotenv
load_dotenv()

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image using Google Cloud Vision API.
    
    :param image_path: Path to the image file (e.g., "images/dni.jpg")
    :return: Extracted text as a string
    """
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Read the image file into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create a Vision API Image object
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)

    # Handle errors
    if response.error.message:
        raise Exception(f"Google Vision API Error: {response.error.message}")

    # Return full text annotation (all text found)
    return response.full_text_annotation.text

def extract_numbers_from_text(text: str) -> list:
    """
    Extracts all numbers from the given text.
    
    :param text: Input text from which to extract numbers
    :return: List of extracted numbers as strings
    """
    import re
    return re.findall(r'\d+', text)

if __name__ == "__main__":
    try:
        text = extract_text_from_image("/home/jorge/Downloads/prueba/checkid/dni2.png")
        print("Extracted text:\n", text)
        print(f"Extracted numbers: {extract_numbers_from_text(text)}")
    except Exception as e:
        print("Error:", e)