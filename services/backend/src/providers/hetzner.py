from hcloud import Client, APIException
from hcloud.images import Image
from hcloud.server_types import ServerType
from hcloud.servers import BoundServer
from hcloud.ssh_keys import SSHKey, BoundSSHKey

from src.schemas.servers import ServerPrivateSchema, ServerCreateResponseSchema
from src.schemas.users import UserPublicSchema


class Hetzner:
    def __init__(self, token: str):
        self.client = Client(token=token)
        pass

    def create_server(self, server_obj: ServerPrivateSchema, user_obj: UserPublicSchema):
        try:
            ssh_key = self._get_ssh_key(user_obj)
            response = self.client.servers.create(
                name=server_obj.name,
                server_type=ServerType(name=server_obj.type),
                image=Image(name=server_obj.image),
                ssh_keys=ssh_key
            )
            server = response.server
            server_create_response = ServerCreateResponseSchema(
                id=server.id,
                status=server.status
            )
            return server_create_response
        except APIException as e:
            raise e

    def _get_ssh_key(self, user_obj):
        ssh_key_name = f"{user_obj.username}-ssh-key"
        try:
            ssh_key = [self.client.ssh_keys.create(name=ssh_key_name, public_key=user_obj.ssh_key)]
        except APIException as e:
            ssh_key = [self.client.ssh_keys.get_by_name(name=ssh_key_name)]  # Key exists. returning
        return ssh_key

    def update_server(self):
        pass

    def get_server(self, server_obj: ServerPrivateSchema):
        srvr: BoundServer = self.client.servers.get_by_name(server_obj.name)
        return srvr

    def get_servers(self):
        servers = self.client.servers.get_all()
        for server in servers:
            print(f"{server.id=} {server.name=} {server.status=}")

    def delete_server(self, server_obj: ServerPrivateSchema):
        srvr = self.get_server(server_obj)
        return self.client.servers.delete(srvr)
