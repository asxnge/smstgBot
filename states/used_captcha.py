from aiogram.dispatcher.filters.state import State, StatesGroup


class Captcha(StatesGroup):
    user_id = State()
    answer = State()
    who_invite = State()
    text = State()
