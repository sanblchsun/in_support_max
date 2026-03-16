# handlers/echo.py
import asyncio

from filters.fsm_router import state_handler
from states.forms import Form
from loader import dp, bot
from loguru import logger
from utils.message import delete_later


# Эхо хендлер, куда летят текстовые сообщения, в стадии заявки
@state_handler(
    Form.FULL_NAME,
    Form.TELEFON,
    Form.EMAIL,
    Form.FIRMA,
    Form.BEGINNING,
    Form.ATTACH,
    Form.PRIORITY,
    Form.SEND_REQUEST,
)
async def any_state(event, state):

    state_current = await state.get_state()
    if state_current == "full_name":
        await event.message.answer("Введите ваше Имя и Фамилию")
    elif state_current == "telefon":
        await event.message.answer("Введите ваш телефон")
    elif state_current == "email":
        await event.message.answer("Введите ваш e-mail")
    elif state_current == "firma":
        await event.message.delete()
        msg = await event.message.answer(
            "Вы все еще на стадии заполнения заявки. \n\n"
            "Нажмите кнопку\n"
            "или \n"
            "для отмены заявки нажмите на ссылку /cancel"
        )
        asyncio.create_task(delete_later(msg=msg, time_second=3))
    elif state_current == "beginning":
        await event.message.delete()
        msg = await event.message.answer(
            "Вы все еще на стадии заполнения заявки. \n\n"
            "Нажмите кнопку\n"
            "или \n"
            "для отмены заявки нажмите на ссылку /cancel"
        )
        asyncio.create_task(delete_later(msg=msg, time_second=3))


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
