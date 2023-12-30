import os

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Servers
from src.providers.provider import get_cloud_provider
from src.schemas.servers import ServerPublicSchema, ServerCreateResponseSchema
from src.schemas.token import Status

cloud_provider = get_cloud_provider(token=os.environ.get("CLOUD_PROVIDER_TOKEN"))


async def get_servers():
    return await ServerPublicSchema.from_queryset(Servers.all())


async def get_server(server_id) -> ServerPublicSchema:
    return await ServerPublicSchema.from_queryset_single(Servers.get(id=server_id))


async def create_server(server, current_user) -> ServerCreateResponseSchema:
    server_dict = server.dict(exclude_unset=True)
    server_dict["creator_id"] = current_user.id
    server_dict["ssh_key"] = current_user.ssh_key
    try:
        response = await cloud_provider.create_server(server, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    await Servers.create(**server_dict)
    return response


async def update_server(server_id, server, current_user) -> ServerPublicSchema:
    try:
        db_server = await ServerPublicSchema.from_queryset_single(Servers.get(id=server_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Server {server_id} not found")

    if db_server.creator.id == current_user.id or current_user.role == "admin":
        await Servers.filter(id=server_id).update(**server.dict(exclude_unset=True))
        return await ServerPublicSchema.from_queryset_single(Servers.get(id=server_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_server(server_id, current_user) -> Status:
    try:
        db_server = await ServerPublicSchema.from_queryset_single(Servers.get(id=server_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Server {server_id} not found")

    if db_server.creator.id == current_user.id or current_user.role == "admin":
        try:
            response = cloud_provider.delete_server(db_server)
            print(response.status)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
        deleted_count = await Servers.filter(id=server_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Server {server_id} not found")
        return Status(message=f"Deleted server {server_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
