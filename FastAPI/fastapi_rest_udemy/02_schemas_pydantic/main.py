from datetime import datetime
from typing import Optional
import databases
import enum
import sqlalchemy

from pydantic import (
    BaseModel,
    validator
)
from fastapi import FastAPI
from decouple import config
# Helper for hashing passwords
from passlib.context import CryptContext
# email validation
import email_validator


DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:5432/fastapi_clothes"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

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

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/register/", response_model=UserSignOut)
async def create_user(user: UserSignIn):
    # modify the user object by hashing the password
    user.password = pwd_context.hash(user.password)
    q = users.insert().values(**user.dict())
    id_ = await database.execute(q)
    created_user = await database.fetch_one(users.select().where(users.c.id == id_))
    return created_user
