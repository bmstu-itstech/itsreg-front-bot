from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    forward_post = State()
    