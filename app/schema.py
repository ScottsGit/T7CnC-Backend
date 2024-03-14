from pydantic import BaseModel
from typing import TypeVar, Optional

T = TypeVar('T')

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None

class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    

class UserBase(BaseModel):
    email: str
    
class UserIn(UserBase):
    password: str
    



