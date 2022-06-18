from utils.sms_api import Country
from aiogram.dispatcher.filters.state import State, StatesGroup


class ShareYourBalance(StatesGroup):
    user_id = State()
    amount = State()
    confirm = State()


class QiwiKassa(StatesGroup):
    amount = State()

