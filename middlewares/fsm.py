# middlewares/fsm.py
from states.context import FSMContext
from maxapi.filters.middleware import BaseMiddleware
from loguru import logger


class FSMMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):

        logger.debug("Мы сейчас в FSMMiddleware")
        chat_id = None
        user_id = None

        if hasattr(event, "message") and event.message:
            chat_id = event.message.recipient.chat_id
            user_id = event.message.sender.user_id

        if chat_id and user_id:
            # Теперь FSMContext принимает только chat_id и user_id
            data["state"] = FSMContext(chat_id=chat_id, user_id=user_id)

        return await handler(event, data)
