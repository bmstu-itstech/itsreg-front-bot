import os
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from cachetools import TTLCache

from core.handlers.user import register_user
from core.handlers.individual_bot import register_individual_bot
from core.handlers.command_bot import register_command_bot

from core.middlewares.auth import AuthMiddleware
from core.utils.variables import scheduler

from config import load_config


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
    logger.info("Starting bot")
    config = load_config("config.ini")

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    await set_commands(bot)
    dp = Dispatcher(bot, storage=storage)
    dp["context"] = {
        "users": TTLCache(maxsize=sys.maxsize, ttl=60*60*24),   # на один день
    }
    dp.middleware.setup(AuthMiddleware(dp))

    scheduler.start()

    register_user(dp)
    #register_individual_bot(dp)
    register_command_bot(dp)

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
        logger.info("Bot stopped!")
