import requests
from .client import SocialClient, ClientException
from app.base.settings import (
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
)
import logging


logger = logging.Logger(__name__)


class FacebookClient(SocialClient):
    def __init__(self) -> None:
        self.hostname = 'graph.facebook.com'
        self.api = f'https://{self.hostname}/v20.0/{FACEBOOK_PAGE_ID}'

    def send_message(self, message, media_ids=None):
        payload = {
            'message': message,
            'access_token': FACEBOOK_ACCESS_TOKEN,
            'published': True,
        }
        response = requests.post(self.api + '/feed', json=payload)
        if not response.ok:
            print(response)
            logger.error(response)
            raise ClientException
        return True

    def send_media(self, file, file_name=None):
        pass
