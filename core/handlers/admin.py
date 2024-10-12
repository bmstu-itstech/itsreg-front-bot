import asyncio
import logging


from contextlib import suppress
from datetime import datetime, timedelta
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from services.db.repository import Repo
from common.models.role import UserRole
from core.states.Mailing import Mailing
from core.utils.keyboards import *


logger = logging.getLogger(__name__)
mailing_ids = []


async def admin_menu(message: Message, state: FSMContext):
    await message.answer("Админ-панель открыта", reply_markup=get_admin_keyboard())
    await state.finish()


async def admin_menu_call(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите действие", reply_markup=get_admin_keyboard())
    await call.answer()
    await state.finish()


async def statistics(call: CallbackQuery, state: FSMContext, repo: Repo):
    users = await repo.get_users()
    today = datetime.now()

    text = (
        f"Всего в боте: {len(users)}\n"
        f"За сегодня: {len(list(filter(lambda x: x.created_on > today - timedelta(days=1), users)))}\n"
        f"За неделю: {len(list(filter(lambda x: x.created_on > today - timedelta(days=7), users)))}\n"
        f"За месяц: {len(list(filter(lambda x: x.created_on > today - timedelta(days=30), users)))}\n"
    )

    await call.answer()
    await call.message.answer(text, parse_mode="html")
    await state.finish()


async def mailing(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте пост для рассылки")
    await callback.answer()
    await state.set_state(Mailing.forward_post.state)


async def send_messages(message: Message, repo: Repo, mailing_id: int):
    global mailing_ids 

    users = await repo.get_users()
    success = 0
    with_error = 0

    msg = await message.answer(
        "Рассылка запущена\n"
        "Успешно: 0, неудачно: 0",
        reply_markup=get_stop_mailing_keyboard(mailing_id)
    )

    for user in users:
        if mailing_id not in mailing_ids:
            break
        try:
            await message.bot.copy_message(
                user.uuid,
                message.chat.id,
                message.message_id,
                reply_markup=message.reply_markup
            )
            success += 1
            await asyncio.sleep(0.05)

        except BaseException as e:
            logger.info(e)
            with_error += 1
        
        finally:
            if (success + with_error) % 100 == 0:
                await msg.edit_text(
                    "Рассылка запущена\n"
                    f"Успешно: {success}, неудачно: {with_error}",
                    reply_markup=get_stop_mailing_keyboard(mailing_id)
                )

    await msg.edit_text(
        "Рассылка запущена\n"
        f"Успешно: {success}, неудачно: {with_error}"
    )
    if mailing_id in mailing_ids:
        await message.answer("Рассылка завершена")


async def mailing_here_post(message: Message, state: FSMContext, repo: Repo):
    global mailing_ids

    await state.finish()

    mailing_id = hash(datetime.today())
    mailing_ids.append(mailing_id)
    await send_messages(message, repo, mailing_id)


async def stop_mailing(call: CallbackQuery):
    global mailing_ids

    mailing_id = int(call.data.split("_")[-1])
    with suppress(ValueError):
        mailing_ids.remove(mailing_id)
    await call.message.answer("Рассылка остановлена")
    await call.answer()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands="admin", state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(admin_menu_call, Text("admin"), state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(statistics, Text("statistics"), state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(mailing, Text("mailing"), state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(stop_mailing, Text(startswith="stop_mailing"), state="*", role=UserRole.ADMIN)
    dp.register_message_handler(mailing_here_post, content_types=["any"], state=Mailing.forward_post, role=UserRole.ADMIN)
