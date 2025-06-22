from PIL import Image, ExifTags

import os 
import shutil 
import uuid

# Upload DIR
updload_dir = 'uploads'
os.makedirs(updload_dir, exist_ok=True)

def clean_dir() -> None:
    if os.path.exists(updload_dir):
        for archivo in os.listdir(updload_dir):
            path = os.path.join(updload_dir, archivo)
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    else:
        print("Dir didn't exist.")

# Convert images to .png 
def convert_image_to_png(image_path: str) -> str:
    """
    Convierte una imagen a .png si no lo es. Corrige la orientación usando EXIF si es necesario.
    Retorna la ruta de la imagen final (original o convertida).
    """
    _, ext = os.path.splitext(image_path)
    ext = ext.lower()

    if ext in ['.png', '.hex']:
        return image_path

    try:
        with Image.open(image_path) as img:
            try:
                exif = img._getexif()
                if exif:
                    orientation_key = [k for k, v in ExifTags.TAGS.items() if v == 'Orientation']
                    if orientation_key:
                        orientation = exif.get(orientation_key[0])
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
            except Exception as exif_error:
                print(f"Warning: didn't read EXIF code: {exif_error}")

            img = img.convert("RGBA")
            new_path = f"{os.path.splitext(image_path)[0]}.png"
            img.save(new_path, format="PNG")

        os.remove(image_path)  
        return new_path

    except Exception as e:
        print(f"Error, don't convert {image_path}: {e}")
        return image_path

def save_files(data:list) -> list:
    """
    Save files to the system.
    data: list - File data
    return: list - Path to the files
    """
    file_paths = []
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.hex']
    
    for file in data:
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension in valid_extensions:
            file_path = os.path.join(updload_dir, f"{uuid.uuid4()}-{file.filename}")
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)

            # Convert if necesary
            final_path = convert_image_to_png(file_path)
            file_paths.append(final_path)

        else:
            print(f"File: {file.filename} not allowed")
    
    return file_paths

def delete_files(file_paths: list) -> bool:
    """
    Delete files from the system.
    file_paths: list - path to the files
    return: bool - True if the file was deleted
    """
    result = True
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        except Exception as e:
            print(f"Error: {file_path}: {e}")
            result = False

    return result