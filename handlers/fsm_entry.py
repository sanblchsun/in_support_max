# handlers/fsm_entry.py
from loader import dp
from maxapi.types import MessageCreated
from states.context import FSMContext
from fsm_router import handlers


@dp.message_created()
async def fsm_entry(event: MessageCreated):

    chat_id = event.message.recipient.chat_id
    user_id = event.message.sender.user_id # type: ignore

    state = FSMContext(chat_id, user_id) # type: ignore

    current = await state.get_state()

    if not current:
        return

    handler = handlers.get(current)

    if handler:
        await handler(event, state)