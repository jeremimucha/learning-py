from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from fastapi import (
    HTTPException,
)

from db import database
from models import (
    user,
    RoleType
)
from managers.auth import AuthManager


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:

    @staticmethod
    async def register(user_data: dict):
        # Hash the user password
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        # TODO: This seems bad, shouldn't we just return user_do,
        # and let the caller decide how to further process this data?
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data: dict):
        # do == database object
        user_email = user_data['email']
        user_do = await database.fetch_one(user.select().where(user.c.email == user_email))
        if not user_do:
            raise HTTPException(400, "Wrong email or password")  # do not expose that this email does not exist.
        elif not pwd_context.verify(user_data["password"], user_do["password"]):  
            raise HTTPException(400, "Wrong email or password")  # do not expose that this email does not exist.
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_user_by_email(email: str):
        return await database.fetch_all(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id: int):
        await database.execute(user.update().where(user.c.id == user_id).values(role=role))
