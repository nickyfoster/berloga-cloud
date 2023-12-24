from hcloud import Client, APIException
from hcloud.images import Image
from hcloud.server_types import ServerType
from hcloud.servers import BoundServer
from hcloud.ssh_keys import SSHKey, BoundSSHKey

from src.schemas.servers import ServerPrivateSchema


class Hetzner:
    def __init__(self, token: str):
        self.client = Client(token=token)
        pass

    def create_server(self, server_obj: ServerPrivateSchema):
        try:
            ssh_key = None
            if server_obj.ssh_key:
                ssh_key = [self._create_ssh_key(name=f"{server_obj.name}-ssh-key", pub_key=server_obj.ssh_key)]
            response = self.client.servers.create(
                name=server_obj.name,
                server_type=ServerType(name=server_obj.type),
                image=Image(name=server_obj.image),
                ssh_keys=ssh_key
            )
            print(f"response: {response.server}")
        except APIException as e:
            raise e

    def _create_ssh_key(self, name, pub_key) -> BoundSSHKey:
        return self.client.ssh_keys.create(name=name, public_key=pub_key)

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
        self.client.servers.delete(srvr)
