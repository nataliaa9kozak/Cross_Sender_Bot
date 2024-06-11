from abc import ABC, abstractmethod
from functools import wraps
import httpx


class SocialClient(ABC):
    @abstractmethod
    def send_message(self, message, media_ids=None):
        pass

    @abstractmethod
    def send_media(self, file, file_name):
        pass


class ClientException(Exception):
    pass


def handle_client_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPError as e:
            print(e)
    return wrapper
