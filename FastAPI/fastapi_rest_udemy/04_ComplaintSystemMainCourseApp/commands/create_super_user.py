#!/usr/bin/env python3
import asyncclick as click
from pathlib import Path
import sys

_SCRIPT_DIR : Path = Path(__file__).parent.resolve()
sys.path.append(str(_SCRIPT_DIR.parent))

from db import database
from managers.user import UserManager
from models import (
    RoleType
)


@click.command()
@click.option("-f", "--first-name", type=str, required=True)
@click.option("-l", "--last-name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone-number", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-ps", "--password", type=str, required=True)
async def create_user(first_name, last_name, email, phone_number, iban, password):
    user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "iban": iban,
            "password": password,
            "role": RoleType.admin
        }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()


if __name__ == '__main__':
    create_user(_anyio_backend="asyncio")
