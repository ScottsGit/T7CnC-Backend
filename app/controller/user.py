from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schema
from app.service.auth import AuthService
from app.service.user import UserService
from app.database import db
from app.model import *
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import commit_rollback

router = APIRouter()


@router.post("/register/", response_model=schema.UserRegisterResponse)
async def register(user_in: schema.UserIn, db: Session = db):
    db_user = await UserService.find_by_email(user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = AuthService.get_password_hash(user_in.password)
    _user = Users(**user_in.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(_user)
    await commit_rollback()
    return _user


@router.post("/token", response_model=schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = db
):
    user = await UserService.find_by_email(form_data.email)
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
    return {"access_token": access_token, "token_type": "bearer"}


