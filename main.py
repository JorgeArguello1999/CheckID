from fastapi import FastAPI
from routers.v1 import router as v1_router
import uvicorn

from modules import file_handler

# Start APP
app = FastAPI()

# Clean uploads dirs 
print("Cleaning directory")
file_handler.clean_dir()

# Load routers
app.include_router(v1_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1
    )