from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Servers

ServerInSchema = pydantic_model_creator(
    Servers, name="ServerIn", exclude=["creator_id"], exclude_readonly=True)
ServerOutSchema = pydantic_model_creator(
    Servers, name="Server", exclude=[
        "modified_at", "creator.password", "creator.created_at", "creator.modified_at"
    ]
)


class UpdateServer(BaseModel):
    name: Optional[str]
    type: Optional[str]
    ssh_pub_key: Optional[str]
