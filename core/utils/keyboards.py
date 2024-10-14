from aiogram import types


def get_admin_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Рассылка", callback_data="mailing"),
        types.InlineKeyboardButton(text="Статистика", callback_data="statistics"),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_start_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Мои боты", callback_data="my_bots"),
        types.InlineKeyboardButton(text="Создать бота", callback_data="new_bot"),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_my_no_bots_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Вперед!", callback_data="new_bot"),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_bots_keyboard(bots: dict) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text=bot["name"], callback_data=f"bot_{bot['botUUID']}")
        for bot in bots
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_bot_keyboard(bot_obj: dict) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Остановить", callback_data=f"stop_{bot_obj['botUUID']}")
        if bot_obj["status"] == "started" else
        types.InlineKeyboardButton(text="Запустить", callback_data=f"start_{bot_obj['botUUID']}"),
        types.InlineKeyboardButton(text="Рассылка", callback_data="mailing")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_bot_templates_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Индивидуальная регистрация", callback_data="new_bot_template_0"),
        types.InlineKeyboardButton(text="Командная регистрация", callback_data="new_bot_template_1"),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_options_keyboard(added_buttons: list[str]) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text=button, callback_data="pass")
        for button in added_buttons
    ]
    buttons.append(types.InlineKeyboardButton(text="Добавить кнопку", callback_data="add_button"))
    buttons.append(types.InlineKeyboardButton(text="Далее", callback_data="apply_buttons"))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(*buttons)
    return keyboard


def get_skip_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.resize_keyboard = True
    keyboard.add(types.KeyboardButton("Пропустить"))
    return keyboard


def get_empty_keyboard() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def get_yes_no_keyboard() -> types.ReplyKeyboardMarkup:
    buttons = [
        types.KeyboardButton(text="Да", callback_data="yes"),
        types.KeyboardButton(text="Нет", callback_data="no"),
    ]
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.resize_keyboard = True
    keyboard.add(*buttons)
    return keyboard


def get_stop_mailing_keyboard(mailing_id: int) -> types.InlineKeyboardMarkup: 
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Остановить рассылку", callback_data=f"stop_mailing_{mailing_id}")
    ]
    keyboard.add(*buttons)
    return keyboard


def get_cancel_keyboard(callback: str) -> types.InlineKeyboardMarkup: 
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Отменить', callback_data=f'cancel_{callback}'),
    ]
    keyboard.add(*buttons)
    return keyboard
