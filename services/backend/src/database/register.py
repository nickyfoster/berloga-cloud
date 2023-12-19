from typing import Optional

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from src.schemas.users import Users


def register_tortoise(
        app,
        config: Optional[dict] = None,
        generate_schemas: bool = False,
) -> None:
    @app.on_event("startup")
    async def init_orm():
        await Tortoise.init(config=config)
        if generate_schemas:
            await Tortoise.generate_schemas()

        # await create_admin_user()

    @app.on_event("shutdown")
    async def close_orm():
        await Tortoise.close_connections()
