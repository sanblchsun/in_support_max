from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    usr_id = message.from_user.id
    usr_id_str = str(usr_id)
    if usr_id_str in ADMINS:
        text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/firms - Подписаться на уведомленя о заявках",
            "/unsubscribe - Отписаться от всех уведомлений")
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку")

    await message.answer("\n".join(text))
