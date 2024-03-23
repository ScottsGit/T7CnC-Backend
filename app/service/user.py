
from sqlalchemy.future import select
from sqlalchemy import update as sql_update

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
        query = select(Users.id, Users.email).where(Users.id == id)
        return (await db.execute(query)).mappings().one()
    
    @staticmethod
    async def set_plaid_access_token(id:str, token:str, item_id:str):
        query = sql_update(Users).where(Users.id == id).values(
            plaid_access_token=token, item_id=item_id).execution_options(synchronize_session="fetch")
        await db.execute(query)
        return await commit_rollback()
    
    # @staticmethod
    # async def update_password(email: str, password: str):
    #     query = sql_update(Users).where(Users.email == email).values(
    #         password=password).execution_options(synchronize_session="fetch")
    #     await db.execute(query)
    #     await commit_rollback()
        
    # @staticmethod
    # async def get_user_profile(username:str):
    #     query = select(Users.username, 
    #                     Users.email, 
    #                     Person.name, 
    #                     Person.birth,
    #                     Person.sex,
    #                     Person.profile,
    #                     Person.phone_number).join_from(Users,Person).where(Users.username == username)
    #     return(await db.execute(query)).mappings().one()