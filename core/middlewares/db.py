from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from services.db.repository import Repo
from services.db.data import data as db_data


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        data["repo"] = Repo(db_data)

    async def post_process(self, obj, data, *args):
        del data["repo"]
