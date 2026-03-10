# fsm/context.py
from states.user_state import user_states


class FSMContext:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def set(self, state):
        user_states[self.user_id] = state

    async def get(self):
        return user_states.get(self.user_id)

    async def finish(self):
        user_states.pop(self.user_id, None)
