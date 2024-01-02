from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import File

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Directorio donde se encuentran tus plantillas HTML
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.post("/")
async def home():
    return {
        "message": "Welcome to Face_Detection API",
        "author": "Jorge Arguello al3x_argu",
    }