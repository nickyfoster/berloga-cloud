from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" RENAME COLUMN "statis" TO "status";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" RENAME COLUMN "status" TO "statis";"""
