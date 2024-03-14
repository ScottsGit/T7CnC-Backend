
from sqlalchemy.future import select
from app.model import Users
from app.database import db



class UserService:

    @staticmethod
    async def find_by_email(email: str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()