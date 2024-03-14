from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class UserRegisterResponse(UserBase):
    id: int
    email: str

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    email: str
    
class UserIn(UserBase):
    password: str