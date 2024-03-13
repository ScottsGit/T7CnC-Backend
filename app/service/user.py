
from sqlalchemy.future import select
from app.model import Users, Person
from app.database import db



class UserService:

    @staticmethod
    async def get_user_profile(username:str):
        query = select(Users.username)
        return (await db.execute(query)).mappings().one()