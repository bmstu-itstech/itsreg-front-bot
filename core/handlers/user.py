import asyncio

import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ParseMode

from config import config
from core.states.Bots import Bots
from core.states.NewBot import NewBot
from core.utils.keyboards import *

from services.bots import models
from services.bots.api.default import get_bots, get_bot, start_bot, stop_bot, create_bot


async def start(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(
        "Привет! ItsRegFrontBot нужен для создания ботов c регистрацией на мероприятия.\n"
        "Выбери действие ниже",
        reply_markup=get_start_keyboard(),
    )


async def my_bots(call: CallbackQuery, state: FSMContext, token: str):
    await state.finish()

    client = get_bots.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    bots: list[get_bots.Bot] = await get_bots.asyncio(client=client)

    await call.answer()
    if not bots:
        return await call.message.edit_text(
            "У вас нет ботов, давайте создадим новый!",
            reply_markup=get_my_no_bots_keyboard(),
        )
    await call.message.edit_text(
        "Ваши боты",
        reply_markup=get_bots_keyboard(bots)
    )
    await state.set_state(Bots.here_click)
    await state.update_data(bots=bots)


async def my_bot(call: CallbackQuery, state: FSMContext):
    bot_uuid = "_".join(call.data.split("_")[1:])
    data = await state.get_data()
    bots = data["bots"]
    bot_obj = [bot for bot in bots if bot.bot_uuid == bot_uuid][0]
    await state.update_data(bot_obj=bot_obj)
    await call.message.edit_text(
        "Настройки бота",
        reply_markup=get_bot_keyboard(bot_obj),
    )
    await state.finish()


async def start_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])

    client = start_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await start_bot.asyncio(client=client, uuid=bot_uuid)

    await call.answer("Запрос на старт отправлен!")
    await asyncio.sleep(3)

    client = get_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    bot_obj: models.Bot = await get_bot.asyncio(uuid=bot_uuid, client=client)
    await call.message.edit_reply_markup(get_bot_keyboard(bot_obj))


async def stop_my_bot(call: CallbackQuery, token: str):
    bot_uuid = "_".join(call.data.split("_")[1:])

    client = stop_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await stop_bot.asyncio(client=client, uuid=bot_uuid)

    await call.answer("Запрос на остановку отправлен!")
    await asyncio.sleep(3)

    bot_obj: models.Bot = await get_bot.asyncio(uuid=bot_uuid, client=client)
    await call.message.edit_reply_markup(get_bot_keyboard(bot_obj))


async def mailing_my_bot(call: CallbackQuery):
    await call.answer("В разработке (:")


async def new_bot(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer()
    await call.message.edit_text(
        "Отправьте токен бота. <a href='https://youtu.be/dQw4w9WgXcQ?si=SRYl9NpeR7VC4_Gy'>Инструкция по получению</a>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=None,
    )
    await state.set_state(NewBot.here_token)


async def new_bot_here_token(message: Message, state: FSMContext):
    res = requests.get(f"https://api.telegram.org/bot{message.text}/getMe")
    if res.status_code != 200:
        return await message.answer("Токен не валидный, попробуйте еще раз")
    await state.update_data(token=message.text)
    await message.answer("Отправьте юзернейм или ссылку на бота")
    await state.set_state(NewBot.here_username)


async def new_bot_here_username(message: Message, state: FSMContext):
    if message.text.startswith("https://t.me/"):
        username = message.text.split("/")[-1]
    elif message.text.startswith("@"):
        username = message.text[1:]
    else:
        username = message.text
    await state.update_data(username=username)
    await message.answer("Отправьте название бота, которое будет отображаться в интерфейсе")
    await state.set_state(NewBot.here_name)


async def new_bot_here_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Выберите, какого бота надо создать",
        reply_markup=get_bot_templates_keyboard(),
    )
    await state.set_state(NewBot.here_template)


async def new_bot_here_template(call: CallbackQuery, state: FSMContext):
    template = int(call.data.split("_")[-1])
    if template == 0:
        await call.answer()
        await call.message.edit_text("Введите текст стартового сообщения", reply_markup=None)
        await state.set_state(NewBot.here_start_text)
    elif template == 1:
        return await call.answer("В разработке (:")


async def new_bot_here_start_text(message: Message, state: FSMContext):
    await state.update_data(start_text=message.text)
    await message.answer("Введите текст для вопроса ввода ФИО")
    await state.set_state(NewBot.here_name_text)


async def new_bot_here_name_text(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        await state.update_data(name_text=None)
    else:
        await state.update_data(name_text=message.text)
    await message.answer("Введите текст для вопроса ввода ГРУППЫ")
    await state.set_state(NewBot.here_group_text)


async def new_bot_here_group_text(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        await state.update_data(group_text=None)
    else:
        await state.update_data(group_text=message.text)
    await message.answer(
        "Введите текст для вопроса-подтверждения",
        reply_markup=get_empty_keyboard(),
    )
    await state.set_state(NewBot.here_apply_text)


async def new_bot_here_apply_text(message: Message, state: FSMContext):
    await state.update_data(apply_text=message.text)
    await message.answer(
        "Добавьте кнопки, если требуется. Если не нужны, просто нажмите далее",
        reply_markup=get_options_keyboard([]),
    )
    await state.update_data(options=[])
    await state.set_state(NewBot.here_button)


async def new_bot_add_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(NewBot.here_button_text)
    msg = await call.message.edit_text("Введите текст кнопки", reply_markup=None)
    await state.update_data(btn_msg_id=msg.message_id)


async def new_bot_add_button_here_text(message: Message, state: FSMContext):
    data = await state.get_data()
    data["options"].append(message.text)
    await state.set_data(data)
    await state.set_state(NewBot.here_button)
    await message.delete()
    await message.bot.edit_message_text(
        "Добавьте кнопки",
        message.chat.id,
        data["btn_msg_id"],
        reply_markup=get_options_keyboard(data["options"]),
    )


async def new_bot_apply_buttons(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Введите текст финального сообщения")
    await state.set_state(NewBot.here_final_text)



async def new_bot_here_final_text(message: Message, state: FSMContext, token: str):
    await state.update_data(final_text=message.text)
    data = await state.get_data()

    blocks = [
        models.Block(type=models.BlockType.MESSAGE,  state=1, next_state=2, title="Приветствие", text=data["start_text"]),
        models.Block(type=models.BlockType.QUESTION, state=2, next_state=3, title="ФИО",         text=data["name_text"]),
        models.Block(type=models.BlockType.QUESTION, state=3, next_state=4, title="Группа",      text=data["group_text"]),
        models.Block(type=models.BlockType.MESSAGE,  state=4, next_state=0, title="Финал",       text=data["final_text"]),
    ]
    entries = [
        models.EntryPoint(key="start", state=1)
    ]

    client = create_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await create_bot.asyncio(client=client, body=create_bot.PostBots(
        data["username"],
        data["name"],
        data["token"],
        entries,
        blocks,
    ))

    await message.answer("Бот создан!")
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(my_bots, Text("my_bots"), state="*")
    dp.register_callback_query_handler(my_bot, Text(startswith="bot"), state=Bots.here_click)
    dp.register_callback_query_handler(start_my_bot, Text(startswith="start"), state="*")
    dp.register_callback_query_handler(stop_my_bot, Text(startswith="stop"), state="*")
    dp.register_callback_query_handler(mailing_my_bot, Text(startswith="mailing"), state="*")
    dp.register_callback_query_handler(new_bot, Text("new_bot"), state="*")
    dp.register_message_handler(new_bot_here_token, state=NewBot.here_token)
    dp.register_message_handler(new_bot_here_username, state=NewBot.here_username)
    dp.register_message_handler(new_bot_here_name, state=NewBot.here_name)
    dp.register_callback_query_handler(new_bot_here_template, Text(startswith="new_bot_template"), state=NewBot.here_template)
    dp.register_message_handler(new_bot_here_start_text, state=NewBot.here_start_text)
    dp.register_message_handler(new_bot_here_name_text, state=NewBot.here_name_text)
    dp.register_message_handler(new_bot_here_group_text, state=NewBot.here_group_text)
    dp.register_message_handler(new_bot_here_apply_text, state=NewBot.here_apply_text)
    dp.register_callback_query_handler(new_bot_add_button, Text("add_button"), state=NewBot.here_button)
    dp.register_message_handler(new_bot_add_button_here_text, state=NewBot.here_button_text)
    dp.register_callback_query_handler(new_bot_apply_buttons, Text("apply_buttons"), state=NewBot.here_button)
    dp.register_message_handler(new_bot_here_final_text, state=NewBot.here_final_text)
