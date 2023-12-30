from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Servers

ServerCreateSchema = pydantic_model_creator(
    Servers,
    name="ServerIn",
    exclude=("creator_id", "public_ip"),
    exclude_readonly=True
)

ServerPublicSchema = pydantic_model_creator(
    Servers,
    name="Server",
    exclude=(
        "modified_at", "creator.password", "creator.created_at", "creator.modified_at",
        "creator.role", "creator.full_name", "creator.ssh_key"
    )
)
ServerPrivateSchema = pydantic_model_creator(
    Servers,
    name="User",
    optional=("created_at", "modified_at")
)


class ServerUpdateSchema(BaseModel):
    name: Optional[str]
    type: Optional[str]
    status: Optional[str]
    public_ip: Optional[str]


class ServerCreateResponseSchema(BaseModel):
    id: str
    status: str
