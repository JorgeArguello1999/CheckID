from fastapi import APIRouter

router = APIRouter()

@router.get("/upload")
async def method_get():
    return 0