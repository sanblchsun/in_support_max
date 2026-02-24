import asyncio
from functools import partial
from .send_mail import send_email_with_attachment


async def send_email_in_executor(**kwargs):
    """
    Асинхронный вызов синхронной функции отправки почты.
    Работает НЕ блокируя event loop, прогресс-бар остаётся живым.
    """
    loop = asyncio.get_running_loop()
    func = partial(send_email_with_attachment, **kwargs)
    return await loop.run_in_executor(None, func)
