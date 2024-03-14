
from sqlalchemy.future import select
from app.model import Users
from app.database import db



class UserService:

    @staticmethod
    async def get_user(email:str):
        query = select(Users.email)
        return (await db.execute(query)).mappings().one()