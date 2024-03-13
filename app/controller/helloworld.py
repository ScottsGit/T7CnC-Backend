
from fastapi import APIRouter


router = APIRouter(
    prefix="/helloworld",
    tags=['Hello World']
)

@router.get("/")
async def home():
    return "Hello World"

