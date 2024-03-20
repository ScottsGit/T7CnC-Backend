from pydantic import BaseModel
from typing import TypeVar, Optional

T = TypeVar('T')

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PlaidToken(BaseModel):
    plaid_token: str
    token_type: str
    
class PlaidPublicTokenIn(BaseModel):
    public_token: str 
    
class AccessTokenResponse(BaseModel):
    access_token: str
    item_id: str

class UserBase(BaseModel):
    email: str

class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserInDBBase):
    hashed_password: str
    
class UserIn(UserBase):
    password: str



