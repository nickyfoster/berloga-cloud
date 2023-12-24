from src.providers.hetzner import Hetzner


def get_cloud_provider(token: str):
    return Hetzner(token)
