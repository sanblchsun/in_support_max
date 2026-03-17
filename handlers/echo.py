# handlers/echo.py
import asyncio
from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from states.forms import Form
from loader import dp, bot
from loguru import logger
from utils.message_manager import delete_later


# Эхо хендлер, куда летят текстовые сообщения, в стадии заявки
@dp.message_created(
    F.message.body.attachments,
    Form.full_name,
    Form.telefon,
    Form.e_mail,
    Form.firma,
)
async def any_state(event: MessageCreated, context: MemoryContext):

    state_current = await context.get_state()
    msg = event
    if state_current is Form.full_name:
        msg = await event.message.answer(
            "Вложение ошибочное. Введите ваше Имя и Фамилию"
        )
    elif state_current is Form.telefon:
        msg = await event.message.answer("Вложение ошибочное. Введите ваш телефон")
    elif state_current is Form.e_mail:
        msg = await event.message.answer("Вложение ошибочное. Введите ваш e-mail")
    elif state_current == Form.firma:
        msg = await event.message.answer("Вложение ошибочное. Введите ваш e-mail")
    else:
        logger.debug(
            f"в any_state не обработанное сообщение. Состоняе {state_current} тип {type(state_current)}"
        )
    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=3))


# Эхо хендлер, куда летят ВСЕ сообщения, без стадии заявка
@dp.message_created()
async def no_state(event: MessageCreated, context: MemoryContext):

    mid = event.model_dump().get("message").get("body").get("mid")
    try:
        await bot.delete_message(message_id=mid)
    except Exception as e:
        logger.error(e)
    await event.message.delete()
    msg = await event.message.answer(
        """Начните заполнять заявку, нажимая на /start .
    Или отмените активную заявку на любой стадии, нажимая на /cancel"""
    )

    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))
