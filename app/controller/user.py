from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schema import ResponseSchema
from app.service.user import UserService
from app.schema import *
from app.service.auth import AuthService

router = APIRouter(
    prefix="/api/users",
    tags=['user']
)


@router.get("/{user_email}", response_model=ResponseSchema)
async def read_user_by_id(
    user_email: str, current_user: UserInDB = Depends(AuthService.get_current_user)):
    
    user = await UserService.find_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return ResponseSchema(detail="Successfully!", result=user)