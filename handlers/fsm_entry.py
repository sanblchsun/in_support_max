# handlers/fsm_entry.py

from loader import dp
from maxapi.types import MessageCreated
from states.context import FSMContext
from fsm_router import handlers, any_state_handlers, no_state_handlers


@dp.message_created()
async def fsm_entry(event: MessageCreated, state: FSMContext):

    current = await state.get_state()

    # --- нет состояния ---
    if current is None:
        for handler in no_state_handlers:
            await handler(event, state)
        return

    # --- конкретный state ---
    handler = handlers.get(current)

    if handler:
        await handler(event, state)
        return

    # --- любой state ---
    for handler in any_state_handlers:
        await handler(event, state)