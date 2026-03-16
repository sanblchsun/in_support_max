import asyncio
from loader import bot
from loguru import logger


async def delete_later(msg, time_second: int):

    await asyncio.sleep(time_second)
    mid = msg.model_dump().get("message").get("body").get("mid")
    try:
        await bot.delete_message(message_id=mid)
    except Exception as e:
        logger.error(e)
