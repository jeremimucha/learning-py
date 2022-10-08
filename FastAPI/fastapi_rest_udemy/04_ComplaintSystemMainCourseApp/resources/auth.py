from schemas.request.user import (
    UserRegisterIn,
    UserLoginIn,
)
from fastapi import APIRouter

from managers.user import UserManager


# Routers are a proxy to the `app` object defined in the main.py.
# This lets us create post/get endpoints, while avoiding a cyclic dependency/import.
router = APIRouter(tags=["Auth"])


# Registration logic
#
# On registration we perform the following actions:
# 1. We accept the registration request (this is here - the router.post('/register/') handles this),
# 2. The request needs to be processed by the UserManager (in this case), to e.g. hash the user password
#    and perform any additional validation.
# 3. This is than chained to the AuthManager, which encodes the token.
# 4. We then pass the encoded tocken back as a request response.

@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post("/login/", status_code=201)
async def login(user_data: UserLoginIn):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
