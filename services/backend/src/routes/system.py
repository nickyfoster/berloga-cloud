from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.utils.create_admin import create_admin_user

router = APIRouter()


@router.get("/create_admin")
async def create_admin():
    status_code, response = await create_admin_user()

    if status_code == status.HTTP_200_OK:
        return JSONResponse(status_code=status_code, content={"message": response})
    else:
        raise HTTPException(status_code=status_code, detail=response)
