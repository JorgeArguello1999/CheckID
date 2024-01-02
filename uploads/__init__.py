from fastapi import APIRouter
from uploads import route

router = APIRouter()
router.include_router(route.router)