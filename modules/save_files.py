import os 
import shutil 

# Upload DIR
updload_dir = 'uploads'
os.makedirs(updload_dir, exist_ok=True)

def save_files(data:list) -> list:
    file_paths = []
    for file in data:
        file_path = os.path.join(updload_dir, file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(file_path)
        
    return file_paths

