# handlers/cancel.py
from maxapi import F
from maxapi.context import MemoryContext
from loader import dp, bot
from maxapi.types import Command, MessageCreated
from loguru import logger
from utils.message_manager import delete_messages
from utils.timeout_manager import cancel_timeout


@dp.message_created(Command("cancel"))
async def bot_cancel(event: MessageCreated, context: MemoryContext):
    state_data = await context.get_data()
    logger.debug(f"state_data: {state_data}")
    await cancel_timeout(event=event)
    await delete_messages(bot=bot, event=event)
    await context.clear()
    await event.message.answer("Вы отменили заявку. Начните заново: /start")


@dp.message_callback(F.callback.payload == "del_current_request")
async def action_bot_cancel(event: MessageCreated, context: MemoryContext):

    state_data = await context.get_data()
    logger.debug(f"state_data: {state_data}")
    # await bot_cancel(event=event, context=context)
    await cancel_timeout(event=event)
    await delete_messages(bot=bot, event=event)
    await context.clear()
    await event.message.answer("Вы отменили заявку. Начните заново: /start")