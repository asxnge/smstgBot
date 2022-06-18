from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import config

bot = Bot(token=config.config("bot_token"), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
vip = Dispatcher(bot, storage=storage)
