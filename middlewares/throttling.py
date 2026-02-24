import logging

import emoji
from aiogram import types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from keyboards.default.buttons import send_request_yes_no_def


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    async def on_process_message(self, message: types.Message, data: dict):
#         logging.info(f"""message_id {message.message_id}:
# {data}
# """)
        if message.text == "/start" and data['raw_state'] is not None:
            await message.delete()
            await message.answer("""Вы отправили команду /start
            Но вы уже в стадии активной заявки""")
            raise CancelHandler()
        elif (message.text is not None and message.text != "/cancel" and
              data['raw_state'] in ['Form:priority', 'Form:attach']):
            await message.delete()
            await message.answer("""Нажмите кнопку
            или
        для отмены заявки, нажмите на ссылку /cancel""")
            raise CancelHandler()
        elif ( not (message.text in ["Отправить заявку \U0001FAE1", "Отказаться \U0001F644",
                                     "/cancel", "/start"] )
        and data['raw_state'] == 'Form:send_request'):
            await message.delete()
            keyboard = send_request_yes_no_def()
            await message.answer("""Нажмите кнопку
            или
        для отмены заявки, нажмите на ссылку /cancel""", reply_markup=keyboard)
            raise CancelHandler()




