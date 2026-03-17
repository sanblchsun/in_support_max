# utils/message_manager.py
import asyncio
from loguru import logger
from maxapi.context import MemoryContext


async def add_message(context: MemoryContext, message):
    try:
        data = await context.get_data()

        mid = message.model_dump().get("message").get("body").get("mid")

        if mid:
            messages = data.get("messages", [])
            messages.append(mid)
            await context.update_data(messages=messages)
    except Exception as e:
        logger.error(f"add messsage error: {e}")


async def delete_messages(bot, context):

    data = await context.get_data()
    messages = data.get("messages", [])

    for mid in messages:
        try:
            await bot.delete_message(message_id=mid)
        except Exception:
            pass

    await context.update_data(messages=[])


async def delete_later(bot, msg, time_second: int):

    await asyncio.sleep(time_second)
    mid = msg.model_dump().get("message").get("body").get("mid")
    try:
        await bot.delete_message(message_id=mid)
    except Exception as e:
        ...
