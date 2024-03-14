from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from datetime import datetime, timezone, timedelta
from typing import Optional

from app import schema
from app.database import db
from app.service.user import UserService
from app.config import SECRET_KEY, ALGORITHM



class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = db
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = schema.TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = UserService.find_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user


    @staticmethod
    def get_password_hash(password: str):
        return AuthService.pwd_context.hash(password)


    @staticmethod
    def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt