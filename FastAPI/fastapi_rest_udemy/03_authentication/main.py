from datetime import datetime, timedelta
from typing import Optional
import databases
from databases.interfaces import Record
from starlette.requests import Request
import enum
import sqlalchemy

from pydantic import (
    BaseModel,
    validator
)
from fastapi import (
    FastAPI,
    HTTPException,
    Depends
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from decouple import config
# Helper for hashing passwords
from passlib.context import CryptContext
# email validation
import email_validator
# authentication using JWT/oauth2
import jwt


DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:5432/fastapi_clothes"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


class UserRole(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("full_name", sqlalchemy.String(200)),
    sqlalchemy.Column("phone", sqlalchemy.String(13)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "last_modified_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column("role", sqlalchemy.Enum(UserRole), nullable=False, server_default=UserRole.user.name)
)


class ColorEnum(enum.Enum):
    pink = "pink"
    black = "black"
    white = "white"
    yellow = "yellow"


class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"

clothes = sqlalchemy.Table(
    "clothes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(120)),
    sqlalchemy.Column("color", sqlalchemy.Enum(ColorEnum), nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Enum(SizeEnum), nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(255)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "last_modified_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    ),
)


# pydantic allows to strongly type member fields,
# and include validation logic in the type.
class EmailField(str):

    # __get_validators__ needs to return all validators
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_email
    
    # validation logic is encapsulated in a classmethod.
    @classmethod
    def validate_email(cls, v) -> str:
        try:
            email_validator.validate_email(v)
            return v
        except email_validator.EmailNotValidError:
            # pydantic defines that if we want to return an `HTML 422 Error: Unprocessable Entity` error
            # we need to raise ValueError
            raise ValueError(f"Invalid email: {v}")


# pydantic allows to define strongly typed models.
# These need to match exactly the database table models,
# i.e. the field names, must match the corresponding table rows.
class UserBase(BaseModel):
    # email: str
    email: EmailField
    full_name: Optional[str]

    # # pydantic allows for member data validation.
    # # Adding a classmethod decorated with `@validate("<field-name>")`
    # # will run when a given member is being set.
    # @validator("email")
    # def validate_email(cls, v):
    #     try:
    #         email_validator.validate_email(v)
    #         return v
    #     except email_validator.EmailNotValidError:
    #         # pydantic defines that if we want to return an `HTML 422 Error: Unprocessable Entity` error
    #         # we need to raise ValueError
    #         raise ValueError

    # Validation can also be done in the model class itself.
    # This is more ad-hoc and doesn't facilitate reuse, but can be convenient can justified sometimes.
    @validator("full_name")
    def validate_full_name(cls, v):
        try:
            first_name, last_name = v.split(" ")
            return v
        except ValueError:
            raise ValueError("Please provide first and last name")

# Convention:
# - request schemas (models) should have an "In" suffix,
# - response schemas (models) should have an "Out" suffix,
class UserSignIn(UserBase):
    password: str


# This type will be used as a response to a `post` method.
# We might want to define custom response models, that differ from
# the data provided by the user, or include additional data.
# This is done e.g. to avoid exposing sensitive information like passwords,
# and to provide some additional information that might be valuable to the
# user - e.g. some infromation about the request - the time it took, etc.
#
# This type is specified in the `@app.post(..., response_model=)` decorator
class UserSignOut(UserBase):
    phone: Optional[str]
    created_at: datetime
    last_modified_at: datetime


app = FastAPI()
# Cryptographic context for password validation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authentication using JSON Web Token
def create_access_token(user: Record):
    try:
        # Define a payload to decode - containing user_id and expiration date.
        # Just for demonstration - use relatively short expiration time.
        payload = {"sub": user['id'], "exp": datetime.utcnow() + timedelta(minutes=5)}
        return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
    except Exception as ex:
        # Catch the exception just to log an re-raise it
        raise

# Extend the HTTPBearer class with the custom authentication logic.
# This can be used to add JWT authentication/authorization.
class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        # First defer to HTTPBearer - it will validate if the request
        # carries an expected `Authorization` header with a `Bearer` scheme.
        # If it does, it will return HTTPAuthorizationCredentials carrying
        # the scheme (`Bearer`), and credentials - JWT encoded.
        res = await super().__call__(request)

        try:
            # Next we decode the payload we received, use the same secret and algorithm as before.
            # Note that here we're specifying a list of algorithms, not just one that we used.
            payload = jwt.decode(res.credentials, config("JWT_SECRET"), algorithms=["HS256"])
            # structure of the payload is the same, as we defined in the `create_access_token` function.
            sub = payload["sub"]
            user = await database.fetch_one(users.select().where(users.c.id == sub))
            # We bind the user to the `request state`.
            # The request state can be used to carry arbitrary custom data (?).
            request.state.user = user
            return payload
        except jwt.ExpiredSignatureError as ex:
            # The frontend will redirect the user to the login page and force reauthentication
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")

oauth2_scheme = CustomHTTPBearer()


def is_admin(request: Request) -> bool:
    user = request.state.user
    if not user or user['role'] not in (UserRole.admin, UserRole.super_admin):
        raise HTTPException(403, "You do not have permissions to access this resource.")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/clothes/", dependencies=[Depends(oauth2_scheme)])
async def get_all_clothes(request: Request):
    # The `request` argument here is optional - it can be added to any entrypoint method, if we need
    # access to the request data.
    # It can be used to get access to the state data - e.g. in this case the user:
    user = request.state.user
    print(user)
    return await database.fetch_all(clothes.select())


class ClothesBase(BaseModel):
    name: str
    color: str
    size: SizeEnum
    color: ColorEnum


class ClothesIn(ClothesBase):
    pass

class ClothesOut(ClothesBase):
    id: int
    created_at: datetime
    last_modified_at: datetime


# User authorization.
# - Here we specify that this particular endpoint can be accessed only by users meeting the `is_admin` requirement.
@app.post(
    "/clothes/",
    response_model=ClothesOut,
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],   # <- `is_admin` is specified as a dependency.
    status_code=201,    # status code indicating a valid response
)
async def create_clothes(clothes_data: ClothesIn):
    id_ = await database.execute(clothes.insert().values(**clothes_data.dict()))
    return await database.fetch_one(clothes.select().where(clothes.c.id == id_))


# @app.post("/register/", response_model=UserSignOut)
# We an no longer define the response_model - we're returning just a JWT token
@app.post("/register/", status_code=201)
async def create_user(user: UserSignIn):
    # modify the user object by hashing the password
    user.password = pwd_context.hash(user.password)
    user_dict = user.dict()
    # Just a hack to be able to create an admin user.
    if user.full_name == "IAm Admin":
        user_dict['role'] = UserRole.admin
    q = users.insert().values(**user_dict)
    id_ = await database.execute(q)
    created_user = await database.fetch_one(users.select().where(users.c.id == id_))
    token = create_access_token(created_user)
    return {"token": token}
