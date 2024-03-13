from pydantic import BaseModel
from datetime import datetime



class Author(BaseModel):
    name: str
    age: int
    
    email: str
    password: str
    jwt_token: str
    plaid_access_token: str
    time_created: datetime 
    time_updated: datetime 

    class Config:
        orm_mode = True