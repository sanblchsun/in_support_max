from aiogram.utils.exceptions import MessageError

from loader import bot


async def msg_delete(message_id_start, message_id_end, message_from_user_id):
    try:
        start_int = int(message_id_start)
        end_int = int(message_id_end)
    except TypeError:
        return
    for i in range(start_int + 1, end_int):
        try:
            await bot.delete_message(chat_id=message_from_user_id, message_id=i)
        except MessageError as e: ...