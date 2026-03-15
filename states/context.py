# states/context.py
from states.storage import storage


class FSMContext:

    def __init__(self, chat_id: int, user_id: int):

        self.key = (chat_id, user_id)

        storage.setdefault(self.key, {"state": None, "data": {}})

    async def set_state(self, state):
        storage[self.key]["state"] = state

    async def get_state(self):
        return storage[self.key]["state"]

    async def update_data(self, **kwargs):
        storage[self.key]["data"].update(kwargs)

    async def get_data(self):
        return storage[self.key]["data"]

    async def clear(self):
        storage.pop(self.key, None)