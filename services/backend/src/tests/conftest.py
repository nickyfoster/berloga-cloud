import pytest
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.main import app

DB_URL = "sqlite://:memory:"


@pytest.fixture(scope="module")
async def init_db():
    Tortoise.init_models(["src.database.models"], "models")
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["src.database.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
