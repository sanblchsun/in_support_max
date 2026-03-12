# middlewares/fsm.py

from states.context import FSMContext
from maxapi.filters.middleware import BaseMiddleware


class FSMMiddleware(BaseMiddleware):
    """
    This middleware handles the FSM context.
    """

    # 1. ADD THIS: Accept the bot instance on initialization.
    def __init__(self, bot):
        self.bot = bot

    async def __call__(self, handler, event, data: dict):
        user_id = None
        chat_id = None

        if hasattr(event, "message") and event.message:
            chat_id = event.message.recipient.chat_id
            user_id = event.message.sender.user_id
        elif hasattr(event, "callback_query") and event.callback_query:
            chat_id = event.callback_query.message.recipient.chat_id
            user_id = event.callback_query.sender.user_id

        # 2. FIX: Use `self.bot` which is guaranteed to exist.
        if user_id and chat_id:
            data["state"] = FSMContext(chat_id=chat_id, user_id=user_id, bot=self.bot)

        return await handler(event, data)
