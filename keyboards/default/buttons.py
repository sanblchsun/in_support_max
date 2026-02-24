from aiogram.types import KeyboardButton,ReplyKeyboardMarkup


def send_request_yes_no_def():
    yes_btn = KeyboardButton(text="""Отправить заявку \U0001FAE1""")
    no_btn = KeyboardButton(text="Отказаться \U0001F644")
    return ReplyKeyboardMarkup(resize_keyboard=True).add(no_btn, yes_btn)