from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import HTTPNotFoundError

import src.crud.users as crud
from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.auth.users import validate_user
from src.schemas.token import Status
from src.schemas.users import UserRegisterSchema, UserPublicSchema, UserPrivateSchema, UserUpdateSchema

router = APIRouter()


@router.post("/register", response_model=UserPublicSchema)
async def create_user(user: UserRegisterSchema) -> UserPublicSchema:
    return await crud.create_user(user)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,  # TODO: set to true for prod
    )

    return response


@router.get(
    "/users/whoami", response_model=UserPublicSchema, dependencies=[Depends(get_current_user)]
)
async def read_users_me(current_user: UserPublicSchema = Depends(get_current_user)):
    return current_user


@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
        user_id: int, current_user: UserPrivateSchema = Depends(get_current_user)
) -> Status:
    return await crud.delete_user(user_id, current_user)


@router.patch(
    "/user/{user_id}",
    response_model=UserPublicSchema,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def update_user(
        user_id: int,
        user_update: UserUpdateSchema,
        current_user: UserPublicSchema = Depends(get_current_user),
) -> UserPublicSchema:
    return await crud.update_user(user_id, user_update, current_user)
