# handlers/echo.py
import asyncio
from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from keyboards.inline.buttons import start
from states.forms import Form
from loader import dp, bot
from loguru import logger
from utils.message_manager import delete_later


@dp.message_created(
    F.message.body.text,
    Form.yes_no_save,
    Form.beginning,
    Form.attach,
    Form.send_request,
)
async def action_insert_in_base(event: MessageCreated, context: MemoryContext):
    msg = await event.message.answer("Сейчас нужно нажать кнопку")
    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))


@dp.message_created(F.message.body.text, Form.attach_yes)
async def action_attach_yes(event: MessageCreated, context: MemoryContext):
    msg = await event.message.answer(
        """Ошибочно набран текст, 
вложите файл или сделайте фото"""
    )
    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))


@dp.message_created(
    F.message.body.text.len() > 300,
    Form.full_name,
    Form.telefon,
    Form.e_mail,
    Form.firma,
    Form.description,
)
async def action_full_name(event: MessageCreated, context: MemoryContext):
    if len(event.message.body.text) > 100:  # type: ignore
        msg = await event.message.answer("""Разрешено не больше 100 знаков.""")
        asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=3))
        return


# Эхо хендлер, куда летят текстовые сообщения, в стадии заявки, с вложениями
@dp.message_created(
    F.message.body.attachments,
    Form.full_name,
    Form.telefon,
    Form.e_mail,
    Form.firma,
    Form.description,
    Form.priority,
    Form.attach,
    Form.send_request,
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
    elif state_current == Form.description:
        msg = await event.message.answer("Вложение ошибочное. Введите текст")
    elif (
        state_current == Form.priority
        or state_current == Form.attach
        or state_current == Form.send_request
    ):
        msg = await event.message.answer("Ошибочное вложение, нажмите кнопку")
    else:
        logger.debug(
            f"в any_state не обработанное сообщение. Состоняе {state_current} тип {type(state_current)}"
        )
    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))


@dp.message_created(F.message.body.text, Form.priority)
async def action_priority(event: MessageCreated, context: MemoryContext):
    msg = await event.message.answer("Ошибочно введен текст, нажмите кнопку")
    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))


# Эхо хендлер, куда летят ВСЕ сообщения, без стадии заявка
@dp.message_created()
async def no_state(event: MessageCreated, context: MemoryContext):

    msg = await event.message.answer(
        """Начните заполнять заявку, нажимая на /start .""", attachments=[start()]
    )

    asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))
