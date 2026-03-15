# handlers/start.py
import random

from base.sqlighter import SQLighter
from loader import dp, bot
from states.context import FSMContext
from keyboards.inline.buttons import request_delete_with_data
from maxapi.types import Attachment, BotStarted, Command, MessageCreated
from maxapi.types import InputMedia
from loguru import logger

from states.forms import Form


async def send_photo(chat_id: int, path: str):
    photo = InputMedia(path)
    return await bot.send_message(chat_id=chat_id, attachments=[photo])


@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, state: FSMContext):

    chat_id = event.message.recipient.chat_id
    user_id = event.message.sender.user_id  # type: ignore

    state = FSMContext(chat_id, user_id)  # type: ignore

    await state.set_state(Form.ONE)

    logger.debug("мы установили state: Form.ONE")
