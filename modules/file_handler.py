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

def save_files(data:list) -> list:
    """
    Save files to the system.
    data: list - File data
    return: list - Path to the files
    """
    file_paths = []
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    for file in data:
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension in valid_extensions:
            file_path = os.path.join(updload_dir, f"{uuid.uuid4()}-{file.filename}")
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(file_path)
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