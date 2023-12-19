from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Servers
from src.schemas.servers import ServerOutSchema
from src.schemas.token import Status


async def get_servers():
    return await ServerOutSchema.from_queryset(Servers.all())


async def get_server(server_id) -> ServerOutSchema:
    return await ServerOutSchema.from_queryset_single(Servers.get(id=server_id))


async def create_server(server, current_user) -> ServerOutSchema:
    server_dict = server.dict(exclude_unset=True)
    server_dict["creator_id"] = current_user.id
    server_obj = await Servers.create(**server_dict)
    return await ServerOutSchema.from_tortoise_orm(server_obj)


async def update_server(server_id, server, current_user) -> ServerOutSchema:
    try:
        db_server = await ServerOutSchema.from_queryset_single(Servers.get(id=server_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Server {server_id} not found")

    if db_server.creator.id == current_user.id:
        await Servers.filter(id=server_id).update(**server.dict(exclude_unset=True))
        return await ServerOutSchema.from_queryset_single(Servers.get(id=server_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_server(server_id, current_user) -> Status:
    try:
        db_server = await ServerOutSchema.from_queryset_single(Servers.get(id=server_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Server {server_id} not found")

    if db_server.creator.id == current_user.id:
        deleted_count = await Servers.filter(id=server_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Server {server_id} not found")
        return Status(message=f"Deleted server {server_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
