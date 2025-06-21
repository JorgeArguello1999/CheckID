from fastapi import FastAPI
import uvicorn

# Routers
from routers.v1 import router as v1_router
from routers.v2 import router as v2_router
from routers.home import router as home_router

from modules import file_handler

from fastapi.middleware.cors import CORSMiddleware

# Start APP
app = FastAPI()

# Middleware
origin = [
    "http://localhost:8000",
    "http://127.0.1:8000",
    "*", # Fix for CORS issues
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clean uploads dirs 
print("Cleaning directory")
file_handler.clean_dir()

# Load routers
app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")

# Home page 
app.include_router(home_router, prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1
    )