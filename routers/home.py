from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    with open("./home/index.html", "r") as file:
        home_page = file.read()

    return home_page