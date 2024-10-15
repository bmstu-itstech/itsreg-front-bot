from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from config import config

from services.auth.models import Authenticated
from services.auth.api.default import register_user, login_user

HTTP_NOT_AUTHORIZED = 401


class AuthMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self):
        super().__init__()
        self.login_client = login_user.Client(base_url=config.auth.base_url)
        self.login_client = register_user.Client(base_url=config.auth.base_url)

    async def pre_process(self, obj, data, *args):
        login = obj.from_user.username
        password = str(obj.from_user.id)
        res: login_user.Response[Authenticated] = await login_user.asyncio_detailed(
            client=self.login_client,
            body=login_user.PostLogin(email=login, password=password)
        )
        if res.status_code == HTTP_NOT_AUTHORIZED:
            await register_user.asyncio_detailed(
                client=self.login_client,
                body=register_user.PostRegister(uuid=login, email=login, password=password)
            )
            res: login_user.Response[Authenticated] = await login_user.asyncio_detailed(
                client=self.login_client,
                body=login_user.PostLogin(email=login, password=password)
            )
        if getattr(res.parsed, "access_token", None):
            data["token"] = res.parsed.access_token

    async def post_process(self, obj, data, *args):
        if hasattr(obj, "token"):
            del data["token"]
