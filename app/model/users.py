
from typing import List, Optional
from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import SQLModel, Field, Relationship

from app.model.mixins import TimeMixin


class Users(SQLModel,TimeMixin,table=True):
    __tablename__ = "users"
    
    id: Optional[str] = Field(None, primary_key=True, nullable=False, index=True)
    email: str = Field(sa_column=Column("email", String, unique=True, nullable=False, index=True))
    hashed_password: str
    
    jwt_token : str
    plaid_access_token : str
    