from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import File

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home_get():
    with open('home/index.html', 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content)

@router.post("/")
async def home():
    return {
        "message": "Welcome to Face_Detection API",
        "author": "Jorge Arguello al3x_argu",
    }