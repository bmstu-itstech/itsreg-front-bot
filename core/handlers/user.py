import asyncio

import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ParseMode

from config import config
from core.states.NewBot import NewBot
from core.utils.functions import get_bot_repr
from core.utils.keyboards import *

from core.handlers import templates

from services.bots import models
from services.bots.api.default import get_bots, get_bot, start_bot, stop_bot, create_bot


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
        f"```=IMPORTDATA(\"{config.bots.base_url}/api/bots/{bot_uuid}/answers?jwtToken={token}\"```\n\n"
        "Так же можно получить ответы в формате CSV. Данный формат поддерживает любое приложение "
        "электронных таблиц (например, Excel). Просто перейдите по ссылке, скопируйте и вставьте в таблицу.\n\n"
        f"```{config.bots.base_url}/api/bots/{bot_uuid}/answers?jwtToken={token}```",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_answers_back_keyboard(bot_uuid),
    )


async def new_bot(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer()
    await call.message.edit_text(
        "Вставьте токен телеграм бота. "
        "О том, что такое токен и как его получить можно узнать "
        "<a href='https://youtu.be/dQw4w9WgXcQ?si=SRYl9NpeR7VC4_Gy'>тут</a>.",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=None,
    )
    await state.set_state(NewBot.here_token)


async def new_bot_here_token(message: Message, state: FSMContext):
    res = requests.get(f"https://api.telegram.org/bot{message.text}/getMe")
    if res.status_code != 200:
        return await message.answer("Это не токен. Попробуйте ещё раз.")
    await state.update_data(bot_token=message.text)
    await message.answer(
        "При создании телеграм-бота @BotFather отправил кроме токена ещё и ссылку вида t.me/your_bot. "
        "Введите эту ссылку."
    )
    await state.set_state(NewBot.here_username)


async def new_bot_here_username(message: Message, state: FSMContext):
    if message.text.startswith("https://t.me/"):
        bot_uuid = message.text.split("/")[-1]
    elif message.text.startswith("@"):
        bot_uuid = message.text[1:]
    else:
        bot_uuid = message.text
    await state.update_data(bot_uuid=bot_uuid)
    await message.answer("Введите название телеграм бота.")
    await state.set_state(NewBot.here_name)


async def new_bot_here_name(message: Message, state: FSMContext):
    await state.update_data(bot_name=message.text)
    await message.answer(
        "Сервис ITS Reg предоставляет возможность создать телеграм-бота по одному из предложенных шаблонов. "
        "Выберите, какой шаблон больше всего подходит под Вашу задачу.",
        reply_markup=get_bot_templates_keyboard(),
    )
    await state.set_state(NewBot.here_template)


async def new_bot_here_template(call: CallbackQuery, state: FSMContext):
    template = int(call.data.split("_")[-1])
    if template == 0:
        await call.answer()
        await call.message.edit_text(
            "Введите текст приветственного сообщения.\n"
            "Например: <i>Приветствую, будущий участник мероприятия!</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=None)
        await state.set_state(NewBot.here_start_text)
    elif template == 1:
        return await call.answer("В разработке (:")


async def new_bot_here_start_text(message: Message, state: FSMContext):
    await state.update_data(start_text=message.text)
    await message.answer(
        "Введите текст для вопроса, в котором у пользователя спрашивается его ФИО.\n"
        "Например: <i>Введите Ваше ФИО (Иванов Иван Иванович).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_name_text)


async def new_bot_here_name_text(message: Message, state: FSMContext):
    await state.update_data(name_text=message.text)
    await message.answer(
        "Введите текст для вопроса, в котором у пользователя его учебная группа.\n"
        "Например: <i>Введите Вашу учебную группу в формате: ИУ13-13Б.</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_group_text)


async def new_bot_here_group_text(message: Message, state: FSMContext):
    await state.update_data(group_text=message.text)
    await message.answer(
        "Введите текст для вопроса-подтверждения регистрации. После выбора утвердительного "
        "ответа на вопрос пользователь оканчивает регистрацию; при выборе отрицательного ответа "
        "пользователь начинает проходить регистрацию заново.\n"
        "\n"
        "Например: <i>Готов участвовать в захватывающем мероприятии (подтверждаю правильность "
        "введённых данных).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_apply_text)


async def new_bot_here_apply_text(message: Message, state: FSMContext):
    await state.update_data(apply_text=message.text)
    await message.answer(
        "Введите текст <i>утвердительно</i> ответа на подтверждение правильности введённых данных.\n"
        "Например: <i>Да!</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_apply_yes_text)


async def new_bot_here_apply_yes_text(message: Message, state: FSMContext):
    await state.update_data(apply_yes_text=message.text)
    await message.answer(
        "Введите текст <i>отрицательного</i> ответа на подтверждение правильности введённых данных.\n"
        "Например: <i>Назад</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_apply_no_text)


async def new_bot_here_apply_no_text(message: Message, state: FSMContext):
    await state.update_data(apply_no_text=message.text)
    await message.answer(
        "Введите текст для финального сообщения бота после окончания регистрации.\n"
        "Например: <i>Спасибо за регистрацию! Ждём на мероприятии 32 февраля в 19:00 в 345 (ГУК).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(NewBot.here_final_text)


async def new_bot_here_final_text(message: Message, state: FSMContext, token: str):
    await state.update_data(final_text=message.text)
    data = await state.get_data()

    body = templates.individual_registration_bot(
        data["bot_uuid"],
        data["bot_token"],
        data["bot_name"],
        data["start_text"],
        data["name_text"],
        data["group_text"],
        data["apply_text"],
        data["apply_yes_text"],
        data["apply_no_text"],
        data["final_text"],
    )

    client = create_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await create_bot.asyncio(client=client, body=body)

    await message.answer("Бот создан!")
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(my_bots, Text("my_bots"), state="*")
    dp.register_callback_query_handler(my_bot, Text(startswith="bot"), state="*")
    dp.register_callback_query_handler(start_my_bot, Text(startswith="start"), state="*")
    dp.register_callback_query_handler(stop_my_bot, Text(startswith="stop"), state="*")
    dp.register_callback_query_handler(mailing_my_bot, Text(startswith="mailing"), state="*")
    dp.register_callback_query_handler(answers_my_bot, Text(startswith="answers"), state="*")
    dp.register_callback_query_handler(new_bot, Text("new_bot"), state="*")
    dp.register_message_handler(new_bot_here_token, state=NewBot.here_token)
    dp.register_message_handler(new_bot_here_username, state=NewBot.here_username)
    dp.register_message_handler(new_bot_here_name, state=NewBot.here_name)
    dp.register_callback_query_handler(new_bot_here_template, Text(startswith="new_bot_template"),
                                       state=NewBot.here_template)
    dp.register_message_handler(new_bot_here_start_text, state=NewBot.here_start_text)
    dp.register_message_handler(new_bot_here_name_text, state=NewBot.here_name_text)
    dp.register_message_handler(new_bot_here_group_text, state=NewBot.here_group_text)
    dp.register_message_handler(new_bot_here_apply_text, state=NewBot.here_apply_text)
    dp.register_message_handler(new_bot_here_apply_yes_text, state=NewBot.here_apply_yes_text)
    dp.register_message_handler(new_bot_here_apply_no_text, state=NewBot.here_apply_no_text)
    dp.register_message_handler(new_bot_here_final_text, state=NewBot.here_final_text)
