from fastapi import APIRouter,Depends,Security

from app.schema import ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from app.service.users import UserService

router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)


