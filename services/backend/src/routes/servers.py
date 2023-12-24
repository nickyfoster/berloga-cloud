from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.servers as crud
from src.auth.jwthandler import get_current_user
from src.schemas.servers import ServerPublicSchema, ServerUpdateSchema, ServerCreateSchema
from src.schemas.token import Status
from src.schemas.users import UserPublicSchema

router = APIRouter()


@router.get(
    "/servers",
    response_model=List[ServerPublicSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_servers():
    return await crud.get_servers()


@router.get(
    "/server/{server_id}",
    response_model=ServerPublicSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_server(server_id: int) -> ServerPublicSchema:
    try:
        return await crud.get_server(server_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Server does not exist",
        )


@router.post(
    "/servers", dependencies=[Depends(get_current_user)]
)
async def create_server(
        server: ServerCreateSchema, current_user: UserPublicSchema = Depends(get_current_user)
) -> ServerPublicSchema:
    return await crud.create_server(server, current_user)


@router.patch(
    "/server/{server_id}",
    dependencies=[Depends(get_current_user)],
    response_model=ServerPublicSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_server(
        server_id: int,
        server: ServerUpdateSchema,
        current_user: UserPublicSchema = Depends(get_current_user),
) -> ServerPublicSchema:
    return await crud.update_server(server_id, server, current_user)


@router.delete(
    "/server/{server_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_server(
        server_id: int, current_user: UserPublicSchema = Depends(get_current_user)
):
    return await crud.delete_server(server_id, current_user)
