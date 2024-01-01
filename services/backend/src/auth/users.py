from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from tortoise.exceptions import DoesNotExist

from src.database.models import Users
from src.schemas.users import UserPrivateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    return await UserPrivateSchema.from_queryset_single(Users.get(username=username))


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    try:
        db_user = await get_user(user.username)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    try:
        verify_password(user.password, db_user.password)
    except UnknownHashError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user

if __name__ == '__main__':
    print(get_password_hash("admin"))