from base.settings import BACKEND_URL
from .client import handle_client_exception
import httpx
from functools import wraps


create_user_url = 'api/register/'
user_exist_url = 'api/user-exist/'
user_configs_url = 'configs/'


class BackendClient:
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient(base_url=BACKEND_URL)

    def requires_authentication(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs['self'].http_client.headers = {'TELEGRAM_ID': kwargs['']}
            return await func(*args, **kwargs)
        return wrapper

    @handle_client_exception
    async def create_user(self, email, telegram_id):
        response = await self.http_client.post(create_user_url, data={
            'email': email,
            'telegram_id': telegram_id,
        })
        response.raise_for_status()

    @handle_client_exception
    async def is_telegram_id_exist(self, telegram_id):
        response = await self.http_client.get(user_exist_url, params={'telegram_id': telegram_id})
        response.raise_for_status()
        return response.json().get('telegram_id')

    @handle_client_exception
    async def is_email_exist(self, email):
        response = await self.http_client.get(user_exist_url, params={'email': email})
        response.raise_for_status()
        return response.json().get('email')

    @handle_client_exception
    async def get_configs(self, telegram_id):
        response = await self.http_client.get(user_configs_url, params={'telegram_id': telegram_id})
        response.raise_for_status()
        return response.json()

    @handle_client_exception
    async def update_config(self, social_media, content, telegram_id):
        print('contnet', content)
        response = await self.http_client.post(user_configs_url, json={'social_media': social_media, 'content': content, 'telegram_id': telegram_id})
        configs = response.json()
        print(configs)
        response.raise_for_status()
        return response.json()
