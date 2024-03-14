from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schema import *
from app.service.auth import AuthService
from app.service.user import UserService
from app.database import db
from app.model import *
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from uuid import uuid4


router = APIRouter()


@router.post("/register/", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: UserIn):
    db_user = await UserService.find_by_email(request_body.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = AuthService.get_password_hash(request_body.password)
    _users_id = str(uuid4())
    _user = Users(**request_body.dict(exclude={"password"}), hashed_password=hashed_password, id=_users_id)
    await UserService.create_user(_user)
    return ResponseSchema(detail="Successfully registered!", result={"user_id": _user.id})


@router.post("/login/access-token", response_model=Token, response_model_exclude_none=True)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    _email = form_data.username
    user = await UserService.find_by_email(_email)
    if not user or not AuthService.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
