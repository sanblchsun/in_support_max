# loader.py
from maxapi import Bot, Dispatcher
from data import config
from maxapi.enums.parse_mode import ParseMode


bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()
