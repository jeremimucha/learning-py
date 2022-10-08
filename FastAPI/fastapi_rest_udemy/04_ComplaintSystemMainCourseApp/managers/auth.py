from datetime import datetime, timedelta
from typing import Optional
from models.enums import RoleType

import jwt
from decouple import config

from starlette.requests import Request
from fastapi import (
    HTTPException,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from models import user
from db import database


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user['id'],
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
        except Exception as ex:
            # TODO: Log the exception
            raise


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config("JWT_SECRET"), algorithms=["HS256"])
            sub = payload["sub"]
            user_data = await database.fetch_one(user.select().where(user.c.id == sub))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user['role'] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if not request.state.user['role'] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if not request.state.user['role'] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
