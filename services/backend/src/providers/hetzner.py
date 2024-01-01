import asyncio

from fastapi import HTTPException
from hcloud import Client, APIException
from hcloud.images import Image
from hcloud.server_types import ServerType
from hcloud.servers import BoundServer
from hcloud.ssh_keys import SSHKey
from sshpubkeys import SSHKey, InvalidKeyError

from src.schemas.servers import ServerPrivateSchema, ServerCreateResponseSchema
from src.schemas.users import UserPublicSchema


class Hetzner:
    def __init__(self, token: str):
        self.client = Client(token=token)
        pass

    async def create_server(self, server_obj: ServerPrivateSchema, user_obj: UserPublicSchema):
        try:
            ssh_key = self.get_ssh_key(user_obj.username)
            ssh_keys = [ssh_key] if ssh_key else []
            response = await asyncio.to_thread(
                self.client.servers.create,
                name=server_obj.name,
                server_type=ServerType(name=server_obj.type),
                image=Image(name=server_obj.image),
                ssh_keys=ssh_keys
            )
            server = response.server
            server_create_response = ServerCreateResponseSchema(
                id=server.id,
                status=server.status
            )
            return server_create_response, response.root_password
        except APIException as e:
            raise HTTPException(
                status_code=400,
                detail="Server name is already used",
            )

    def get_ssh_key(self, username):
        ssh_key_name = f"{username}-ssh-key"
        return self.client.ssh_keys.get_by_name(name=ssh_key_name)

    def create_ssh_key(self, username, ssh_key):
        ssh_key_name = f"{username}-ssh-key"
        try:
            _ssh_key = SSHKey(ssh_key)
            _ssh_key.parse()
        except InvalidKeyError as e:
            raise HTTPException(
                status_code=400,
                detail="Invalid SSH Key provided",
            )
        if self.get_ssh_key(username):
            self.delete_ssh_key(username)
        self.client.ssh_keys.create(name=ssh_key_name, public_key=ssh_key)

    def delete_ssh_key(self, username):
        ssh_key_name = f"{username}-ssh-key"
        ssh_key = self.client.ssh_keys.get_by_name(ssh_key_name)
        ssh_key.delete()

    def update_server(self):
        pass

    def get_server(self, server_obj: ServerPrivateSchema):
        srvr: BoundServer = self.client.servers.get_by_name(server_obj.name)
        return srvr

    # def get_servers(self):
    #     servers = self.client.servers.get_all()
    #     for server in servers:
    #         print(f"{server.id=} {server.name=} {server.status=}")

    def delete_server(self, server_obj: ServerPrivateSchema):
        srvr = self.get_server(server_obj)
        return self.client.servers.delete(srvr)
