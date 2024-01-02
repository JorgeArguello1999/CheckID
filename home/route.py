from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {
        "message": "Welcome to Face_Detection API",
        "author": "Jorge Arguello al3x_argu",
    }