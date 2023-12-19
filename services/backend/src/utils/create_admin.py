import secrets
import string
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
from fastapi import status

from src.database.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    password = "admin"  # TODO remove before production
    return password


async def create_admin_user() -> (int, str):
    try:
        await Users.get(username="admin")
        return status.HTTP_422_UNPROCESSABLE_ENTITY, "Admin user already exists."
    except DoesNotExist:
        admin_password = generate_password()
        password_hash = pwd_context.encrypt(admin_password)
        admin_user = Users(username="admin", password=password_hash, role="admin")
        await admin_user.save()
        return status.HTTP_200_OK, {"status": "admin created", "password": admin_password}
