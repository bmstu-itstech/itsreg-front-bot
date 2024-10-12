import json
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker

from common.models.entry_point import EntryPoint
from common.models.block import Block
from common.models.option import Option
from config import load_config
from core.filters.role import RoleFilter, AdminFilter
from core.handlers.admin import register_admin
from core.handlers.user import register_user
from core.middlewares.db import DbMiddleware
from core.middlewares.role import RoleMiddleware
from core.middlewares.exists_user import ExistsUserMiddleware
from core.utils.variables import scheduler
from services.db.pool_creater import create_pool

from services.api.itsreg import ItsRegApi

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Открыть меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    if os.path.isfile('bot.log'):
        os.remove('bot.log')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        encoding="UTF-8",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    logger.error("Starting bot")
    config = load_config("config.ini")

    storage = MemoryStorage()
    pool: sessionmaker = await create_pool(
        user=config.db.user,
        password=config.db.password,
        address=config.db.address,
        name=config.db.name,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    await set_commands(bot)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
    dp.middleware.setup(ExistsUserMiddleware(pool))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    scheduler.start()

    register_admin(dp)
    register_user(dp)

    try:
        await dp.start_polling(allowed_updates=["message", "callback_query"])
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
