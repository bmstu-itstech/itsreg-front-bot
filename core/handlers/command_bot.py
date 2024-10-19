from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ParseMode

from core.states import CreateBot
from core.utils.keyboards import get_start_keyboard

from services.bots.models.block import Block, BlockType
from services.bots.models.entry_point import EntryPoint
from services.bots.models.option import Option
from services.bots.models.post_bots import PostBots
from services.bots.api.default import create_bot

from config import config


def command_registration_bot(
        *,
        bot_name: str,
        bot_token: str,
        bot_title: str,
        m_greet_text: str,
        q_name_text: str,
        q_group_text: str,
        q_command_name: str,
        q_command_size_text: str,
        q_approve_text: str,
        s_approve_yes_text: str,
        s_approve_no_text: str,
        m_finish_text: str,
) -> PostBots:
    blocks = [
        Block(type=BlockType.MESSAGE,   state=1, next_state=2, title="Приветствие",    text=m_greet_text),
        Block(type=BlockType.QUESTION,  state=2, next_state=3, title="ФИО",            text=q_name_text ),
        Block(type=BlockType.QUESTION,  state=3, next_state=4, title="Группа",         text=q_group_text),
        Block(type=BlockType.QUESTION,  state=4, next_state=5, title="Команда",        text=q_command_name),
        Block(type=BlockType.QUESTION,  state=5, next_state=6, title="Размер команды", text=q_command_size_text),
        Block(type=BlockType.SELECTION, state=6, next_state=6, title="Подтверждение",  text=q_approve_text, options=[
            Option(text=s_approve_yes_text, next_=7),
            Option(text=s_approve_no_text,  next_=2),
        ]),
        Block(type=BlockType.MESSAGE, state=7, next_state=0, title="Конец", text=m_finish_text),
    ]
    entries = [
        EntryPoint(key="start", state=1)
    ]
    mailings = []
    return PostBots(
        bot_uuid=bot_name,
        name=bot_title,
        token=bot_token,
        entries=entries,
        blocks=blocks,
        mailings=mailings,
    )


async def new_bot_here_template(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        "Введите текст приветственного сообщения.\n"
        "Например: <i>Приветствую, будущий участник мероприятия!</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=None)
    await state.set_state(CreateBot.Command.here_start_text)


async def new_bot_here_start_text(message: Message, state: FSMContext):
    await state.update_data(start_text=message.text)
    await message.answer(
        "Введите текст для вопроса, в котором у пользователя спрашивается его ФИО.\n"
        "Например: <i>Введите Ваше ФИО (Иванов Иван Иванович).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_name_text)


async def new_bot_here_name_text(message: Message, state: FSMContext):
    await state.update_data(name_text=message.text)
    await message.answer(
        "Введите текст для вопроса, в котором у капитана команды спрашивается его учебная группа.\n"
        "Например: <i>Введите Вашу (не участников команды!) учебную группу в формате: ИУ13-13Б.</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_group_text)


async def new_bot_here_group_text(message: Message, state: FSMContext):
    await state.update_data(group_text=message.text)
    await message.answer(
        "Введите текст для вопроса названия команды.",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_command_name_text)


async def new_bot_here_command_name(message: Message, state: FSMContext):
    await state.update_data(command_name=message.text)
    await message.answer(
        "Введите текст для вопроса количества человек в команде.",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_command_size_text)


async def new_bot_here_command_size(message: Message, state: FSMContext):
    await state.update_data(command_size=message.text)
    await message.answer(
        "Введите текст для вопроса-подтверждения регистрации. После выбора утвердительного "
        "ответа на вопрос пользователь оканчивает регистрацию; при выборе отрицательного ответа "
        "пользователь начинает проходить регистрацию заново.\n"
        "\n"
        "Например: <i>Готов участвовать в захватывающем мероприятии (подтверждаю правильность "
        "введённых данных).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_apply_text)


async def new_bot_here_apply_text(message: Message, state: FSMContext):
    await state.update_data(apply_text=message.text)
    await message.answer(
        "Введите текст <i>утвердительного</i> ответа на подтверждение правильности введённых данных.\n"
        "Например: <i>Да!</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_apply_yes_text)


async def new_bot_here_apply_yes_text(message: Message, state: FSMContext):
    await state.update_data(apply_yes_text=message.text)
    await message.answer(
        "Введите текст <i>отрицательного</i> ответа на подтверждение правильности введённых данных.\n"
        "Например: <i>Назад</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_apply_no_text)


async def new_bot_here_apply_no_text(message: Message, state: FSMContext):
    await state.update_data(apply_no_text=message.text)
    await message.answer(
        "Введите текст для финального сообщения бота после окончания регистрации.\n"
        "Например: <i>Спасибо за регистрацию! Ждём на мероприятии 32 февраля в 19:00 в 345 (ГУК).</i>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(CreateBot.Command.here_final_text)


async def new_bot_here_final_text(message: Message, state: FSMContext, token: str):
    await state.update_data(final_text=message.text)
    data = await state.get_data()

    body = command_registration_bot(
        bot_name=data["bot_uuid"],
        bot_token=data["bot_token"],
        bot_title=data["bot_name"],
        m_greet_text=data["start_text"],
        q_name_text=data["name_text"],
        q_group_text=data["group_text"],
        q_command_name=data["command_name"],
        q_command_size_text=data["command_size"],
        q_approve_text=data["apply_text"],
        s_approve_yes_text=data["apply_yes_text"],
        s_approve_no_text=data["apply_no_text"],
        m_finish_text=data["final_text"],
    )

    client = create_bot.AuthenticatedClient(token=token, base_url=config.bots.base_url)
    await create_bot.asyncio(client=client, body=body)

    await message.answer(
        "Бот создан!",
        reply_markup=get_start_keyboard(),
    )
    await state.finish()


def register_command_bot(dp: Dispatcher):
    dp.register_callback_query_handler(new_bot_here_template, Text("new_bot_template_command"),
                                       state=CreateBot.Common.here_template)
    dp.register_message_handler(new_bot_here_start_text, state=CreateBot.Command.here_start_text)
    dp.register_message_handler(new_bot_here_name_text, state=CreateBot.Command.here_name_text)
    dp.register_message_handler(new_bot_here_group_text, state=CreateBot.Command.here_group_text)
    dp.register_message_handler(new_bot_here_command_name, state=CreateBot.Command.here_command_name_text)
    dp.register_message_handler(new_bot_here_command_size, state=CreateBot.Command.here_command_size_text)
    dp.register_message_handler(new_bot_here_apply_text, state=CreateBot.Command.here_apply_text)
    dp.register_message_handler(new_bot_here_apply_yes_text, state=CreateBot.Command.here_apply_yes_text)
    dp.register_message_handler(new_bot_here_apply_no_text, state=CreateBot.Command.here_apply_no_text)
    dp.register_message_handler(new_bot_here_final_text, state=CreateBot.Command.here_final_text)
