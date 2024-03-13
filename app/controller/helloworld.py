
from fastapi import APIRouter


router = APIRouter(
    prefix="/helloworld",
    tags=['helloworld']
)

@router.get("/")
async def home():
    return "Hello World"

