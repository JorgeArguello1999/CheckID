from fastapi import APIRouter
from home import route

router = APIRouter()
router.include_router(route.router)