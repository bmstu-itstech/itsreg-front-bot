import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ParseMode

from config import config
from core.utils.functions import get_bot_repr
from core.utils.keyboards import *

from services.bots import models
from services.bots.api.default import get_bots, get_bot, start_bot, stop_bot, delete_bot


async def start(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(
        "Привет! Это бета-версия сервиса ITS Reg - платформы для создания телеграм-ботов.\n"
        "Выберите действие из предложенных.",
        reply_markup=get_start_keyboard(),
    )


async def my_bots(call: CallbackQuery, state: FSMContext, token: str):
    await state.finish()

    client = get_bots.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    bots: list[get_bots.Bot] = await get_bots.asyncio(client=client)

    await call.answer()
    if not bots:
        return await call.message.edit_text(
            "У Вас нет ботов, давайте создадим новый!",
            reply_markup=get_my_no_bots_keyboard(),
        )
    await call.message.edit_text(
        "Список телеграм-ботов.",
        reply_markup=get_bots_keyboard(bots)
    )


async def my_bot(call: CallbackQuery, state: FSMContext, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])

    client = get_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    bot_obj: models.Bot = await get_bot.asyncio(uuid=bot_uuid, client=client)
    await call.message.edit_text(
        get_bot_repr(bot_obj),
        reply_markup=get_bot_keyboard(bot_obj),
        parse_mode=ParseMode.HTML,
    )


async def start_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])

    client = start_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await start_bot.asyncio(client=client, uuid=bot_uuid)

    await call.answer("Запрос на старт отправлен.")
    await asyncio.sleep(3)

    client = get_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    bot_obj: models.Bot = await get_bot.asyncio(uuid=bot_uuid, client=client)
    await call.message.edit_text(
        get_bot_repr(bot_obj),
        reply_markup=get_bot_keyboard(bot_obj),
        parse_mode=ParseMode.HTML,
    )


async def stop_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])

    client = stop_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await stop_bot.asyncio(client=client, uuid=bot_uuid)

    await call.answer("Запрос на остановку отправлен.")
    await asyncio.sleep(3)

    bot_obj: models.Bot = await get_bot.asyncio(uuid=bot_uuid, client=client)
    await call.message.edit_text(
        get_bot_repr(bot_obj),
        reply_markup=get_bot_keyboard(bot_obj),
        parse_mode=ParseMode.HTML,
    )


async def mailing_my_bot(call: CallbackQuery):
    await call.answer("В разработке (:")


async def answers_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])
    await call.answer()

    await call.message.edit_text(
        "Чтобы видеть ответы в почти реальном времени в гугл-таблицах, вставьте эту строку в любую ячейку. "
        "Обращаем внимание, что ответы редактировать нельзя.\n\n"
        f"```=IMPORTDATA(\"{config.bots.base_url}/bots/{bot_uuid}/answers?jwtToken={token}\"```\n\n"
        "Так же можно получить ответы в формате CSV. Данный формат поддерживает любое приложение "
        "электронных таблиц (например, Excel). Просто перейдите по ссылке, скопируйте и вставьте в таблицу.\n\n"
        f"```{config.bots.base_url}/bots/{bot_uuid}/answers?jwtToken={token}```",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_answers_back_keyboard(bot_uuid),
    )


async def delete_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])
    client = delete_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await delete_bot.asyncio(client=client, uuid=bot_uuid)
    await call.answer()
    await call.message.edit_text(
        f"Бот успешно {bot_uuid} удалён.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_answers_back_keyboard(bot_uuid),
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(my_bots, Text("my_bots"), state="*")
    dp.register_callback_query_handler(my_bot, Text(startswith="bot"), state="*")
    dp.register_callback_query_handler(start_my_bot, Text(startswith="start"), state="*")
    dp.register_callback_query_handler(stop_my_bot, Text(startswith="stop"), state="*")
    dp.register_callback_query_handler(mailing_my_bot, Text(startswith="mailing"), state="*")
    dp.register_callback_query_handler(answers_my_bot, Text(startswith="answers"), state="*")
    dp.register_callback_query_handler(delete_my_bot, Text(startswith="delete"), state="*")
