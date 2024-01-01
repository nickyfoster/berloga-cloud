import os

from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.providers.provider import get_cloud_provider
from src.schemas.token import Status
from src.schemas.users import UserPublicSchema, UserPrivateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cloud_provider = get_cloud_provider(token=os.environ.get("CLOUD_PROVIDER_TOKEN"))


async def create_user(user) -> UserPublicSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await UserPublicSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserPrivateSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id or current_user.role == "admin":
        if current_user.ssh_key:
            cloud_provider.delete_ssh_key(current_user.username)
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


async def update_user(user_id, user_update, current_user) -> UserPublicSchema:
    try:
        user = await UserPublicSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if user.id == current_user.id or current_user.role == "admin":
        user_update_dict = user_update.dict(exclude_none=True)
        if user_update_dict.get("password"):
            user_update_dict["password"] = pwd_context.encrypt(user_update_dict["password"])
        if user_update_dict.get("ssh_key"):
            if user_update.ssh_key != current_user.ssh_key:
                cloud_provider.create_ssh_key(username=current_user.username, ssh_key=user_update.ssh_key)
        await Users.filter(id=user_id).update(**user_update_dict)
        return await UserPublicSchema.from_queryset_single(Users.get(id=user_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")
