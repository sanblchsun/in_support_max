# handlers/echo.py
import asyncio

from filters.fsm_router import state_handler
from states.forms import Form
from loader import dp, bot
from loguru import logger
from utils.message import delete_later


# Эхо хендлер, куда летят текстовые сообщения, в стадии заявки
@state_handler("*")
async def any_state(event, state):
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

    asyncio.create_task(delete_later(msg=msg, time_second=10))


# Эхо хендлер, куда летят ВСЕ сообщения, без стадии заявка
@state_handler(None)
async def no_state(event, state):

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

    asyncio.create_task(delete_later(msg=msg, time_second=10))
