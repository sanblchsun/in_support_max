# handlers/echo.py
import asyncio
from maxapi import F
from maxapi.context import MemoryContext
from states.forms import Form
from loader import dp, bot
from loguru import logger
from utils.message_manager import delete_later


# Эхо хендлер, куда летят текстовые сообщения, в стадии заявки
@dp.message_created(
    F.message.body.text,
    Form.full_name,
    Form.telefon,
    Form.e_mail,
    Form.firma,
    Form.beginning,
    Form.attach,
    Form.attach,
    Form.send_request,
)
async def any_state(event, context: MemoryContext):

    state_current = await context.get_state()
    if state_current is Form.full_name:
        await event.message.answer("Введите ваше Имя и Фамилию")
    elif state_current is Form.telefon:
        await event.message.answer("Введите ваш телефон")
    elif state_current is Form.e_mail:
        await event.message.answer("Введите ваш e-mail")
    elif state_current == Form.firma:
        await event.message.delete()
        msg = await event.message.answer(
            "Вы все еще на стадии заполнения заявки. \n\n"
            "Нажмите кнопку\n"
            "или \n"
            "для отмены заявки нажмите на ссылку /cancel"
        )
        asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=3))
    elif state_current is Form.beginning:
        await event.message.delete()
        msg = await event.message.answer(
            "Вы все еще на стадии заполнения заявки. \n\n"
            "Нажмите кнопку\n"
            "или \n"
            "для отмены заявки нажмите на ссылку /cancel"
        )
        asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=3))
    else:
        logger.debug(
            f"в any_state не обработанное сообщение. Состоняе {state_current} тип {type(state_current)}"
        )


# Эхо хендлер, куда летят ВСЕ сообщения, без стадии заявка
@dp.message_created()
async def no_state(event, context: MemoryContext):

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
