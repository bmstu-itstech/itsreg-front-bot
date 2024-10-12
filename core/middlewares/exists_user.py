from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from services.db.repository import Repo


class ExistsUserMiddleware(BaseMiddleware):
    def __init__(self, pool):
        self.prefix = "key_prefix"
        self.pool = pool
        super(ExistsUserMiddleware, self).__init__()

    async def on_process_update(self, update: Update, data: dict):
        if "message" in update:
            get_update = update.message
        elif "callback_query" in update:
            get_update = update.callback_query
        else:
            get_update = None

        if get_update is not None and not get_update.from_user.is_bot:
            this_user = get_update.from_user

            db: AsyncSession = self.pool()
            repo = Repo(db)

            await repo.add_user(this_user.id)

            if db:
                await db.close()
