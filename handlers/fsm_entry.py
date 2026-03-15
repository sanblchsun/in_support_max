# handlers/fsm_entry.py
from loader import dp
from maxapi.types import MessageCreated
from states.context import FSMContext
from fsm_router import handlers


@dp.message_created()
async def fsm_entry(event: MessageCreated, state: FSMContext):

    current = await state.get_state()

    if not current:
        return

    handler = handlers.get(current)

    if handler:
        await handler(event, state)