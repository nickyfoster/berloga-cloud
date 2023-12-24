from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users

UserRegisterSchema = pydantic_model_creator(
    Users,
    name="UserRegister",
    exclude_readonly=True
)

UserPublicSchema = pydantic_model_creator(
    Users,
    name="UserPublic",
    exclude=("password", "created_at", "modified_at",)
)

UserPrivateSchema = pydantic_model_creator(
    Users,
    name="UserPrivate"
)


class UserUpdateSchema(BaseModel):
    full_name: Optional[str]
    password: Optional[str]
    ssh_key: Optional[str]
