import asyncio
from utils.message_manager import delete_messages

timeout_tasks: dict[tuple[int, int], asyncio.Task] = {}


def get_key(event):
    return (event.message.recipient.chat_id, event.message.sender.user_id)


async def set_timeout(event, context, bot, seconds: int):

    key = get_key(event)

    if key in timeout_tasks:
        timeout_tasks[key].cancel()

    timeout_tasks[key] = asyncio.create_task(
        _timeout(event, context, bot, key, seconds)
    )


async def _timeout(event, context, bot, key, seconds):

    await asyncio.sleep(seconds)

    try:
        await event.message.answer("⏰ Время истекло. Начните заново: /start")
    except Exception:
        pass

    await delete_messages(bot, event)
    await context.clear()

    timeout_tasks.pop(key, None)


async def cancel_timeout(event):

    key = get_key(event)

    task = timeout_tasks.get(key)

    if task:
        task.cancel()
        timeout_tasks.pop(key, None)
