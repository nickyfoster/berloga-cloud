from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" ADD "statis" VARCHAR(20);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" DROP COLUMN "statis";"""
