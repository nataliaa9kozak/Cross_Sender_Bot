from .client import SocialClient


class InstagramClient(SocialClient):
    def __init__(self) -> None:
        pass

    def send_message(self, message, media_ids=None):
        pass

    def send_media(self, file, file_name=None):
        pass
