# utils/message_manager.py
import asyncio


messages: dict[tuple[int, int], list[str]] = {}


def get_key(event):
    return (event.message.recipient.chat_id, event.message.sender.user_id)


async def add_message(event, message):

    key = get_key(event)

    mid = message.model_dump().get("message").get("body").get("mid")

    if mid:
        messages.setdefault(key, []).append(mid)


async def delete_messages(bot, event):

    key = get_key(event)

    for mid in messages.get(key, []):
        try:
            await bot.delete_message(message_id=mid)
        except Exception:
            pass

    messages.pop(key, None)


async def delete_later(bot, msg, time_second: int):

    await asyncio.sleep(time_second)
    mid = msg.model_dump().get("message").get("body").get("mid")
    try:
        await bot.delete_message(message_id=mid)
    except Exception as e:
        ...
