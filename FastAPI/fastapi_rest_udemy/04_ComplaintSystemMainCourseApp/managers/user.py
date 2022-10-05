from http.client import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError

from db import database
from models import user
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
