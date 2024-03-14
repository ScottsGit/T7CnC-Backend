from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schema import ResponseSchema
from app.service.user import UserService
from app.schema import *
from app.service.auth import AuthService

router = APIRouter(
    prefix="/users",
    tags=['user']
)


@router.get("/{user_id}", response_model=ResponseSchema)
async def read_user_by_id(
    user_id: str, current_user: UserInDB = Depends(AuthService.get_current_user)):
    
    user = await UserService.get_user_profile_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return ResponseSchema(detail="Successfully!", result=UserBase(**user))