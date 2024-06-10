from abc import ABC, abstractmethod


class SocialClient(ABC):
    @abstractmethod
    def send_message(self, message, media_ids=None):
        pass

    @abstractmethod
    def send_media(self, file, file_name):
        pass


class ClientException(Exception):
    pass
