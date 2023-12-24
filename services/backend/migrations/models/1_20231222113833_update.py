from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" ADD "public_ip" VARCHAR(20);
        ALTER TABLE "servers" ADD "image" VARCHAR(20) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" DROP COLUMN "public_ip";
        ALTER TABLE "servers" DROP COLUMN "image";"""
