from schemas.base import UserBase
from models import RoleType


class UserOut(UserBase):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    role: RoleType
    iban: str
