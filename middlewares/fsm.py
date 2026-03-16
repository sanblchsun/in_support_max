# middlewares/fsm.py

from states.context import FSMContext
from maxapi.filters.middleware import BaseMiddleware
from filters.fsm_router import dispatch
from loguru import logger


class FSMMiddleware(BaseMiddleware):

    def __init__(self, bot):
        self.bot = bot

    async def __call__(self, handler, event, data):

        logger.debug("FSMMiddleware")

        chat_id = None
        user_id = None

        if hasattr(event, "message") and event.message:
            chat_id = event.message.recipient.chat_id
            user_id = event.message.sender.user_id

        if chat_id and user_id:

            state = FSMContext(chat_id, user_id, self.bot)
            data["state"] = state

            # FSM dispatch
            result = await dispatch(event, state)

            if result:
                return result

        return await handler(event, data)