import pytest

from src.database.models import Users


@pytest.mark.asyncio
async def test_crud_user(init_db):
    print(Users.get(id="0"))
