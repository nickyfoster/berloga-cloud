from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "servers" DROP COLUMN "ssh_pub_key";
        ALTER TABLE "users" ADD "ssh_key" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "ssh_key";
        ALTER TABLE "servers" ADD "ssh_pub_key" TEXT;"""
