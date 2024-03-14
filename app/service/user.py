
from sqlalchemy.future import select
from app.model import Users
from app.database import db
from app.database import commit_rollback


class UserService:

    @staticmethod
    async def find_by_email(email: str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()
    
    
    @staticmethod
    async def create_user(user: Users):
        db.add(user)
        return await commit_rollback()
         
    @staticmethod
    async def get_user_profile_by_id(id:str):
        query = select(Users).where(Users.id == id)
        return(await db.execute(query)).mappings().one()