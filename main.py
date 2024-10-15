import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import load_config
from core.handlers.user import register_user
from core.middlewares.auth import AuthMiddleware
from core.utils.variables import scheduler

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
    dp.middleware.setup(AuthMiddleware())

    scheduler.start()

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
        logger.info("Bot stopped!")
