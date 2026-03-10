# middlewares/fsm.py
from states.context import FSMContext
from maxapi.filters.middleware import BaseMiddleware

class FSMMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.message.sender.user_id
        data["state"] = FSMContext(user_id)
        return await handler(event, **data)