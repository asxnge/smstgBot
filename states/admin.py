from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminSearch(StatesGroup):
    user_id = State()

class AdminGiveBalance(StatesGroup):
    user_id = State()
    amount = State()
    confirm = State()

class EmailText(StatesGroup):
    text = State()
    action = State()
    down = State()
    down_confirm = State()


class EmailPhoto(StatesGroup):
    photo = State()
    text = State()
    action = State()
    down = State()
    down_confirm = State()

class ButtonsAdd(StatesGroup):
    name = State()
    text = State()
    photo = State()
    confirm = State()

class SMSHubAPI(StatesGroup):
    api = State()
    confirm = State()

class SMSActivateAPI(StatesGroup):
    api = State()
    confirm = State()

class EditQiwiToken(StatesGroup):
    api = State()
    confirm = State()

class EditQiwiNumber(StatesGroup):
    number = State()
    confirm = State()

class EditSecretQiwi(StatesGroup):
    key = State()
    confirm = State()

class RentPercent(StatesGroup):
    time = State()
    percent = State()
    confirm = State()

class AdminActivatePercent(StatesGroup):
    country = State()
    service = State()
    percent = State()
    confirm = State()
