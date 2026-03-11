# states/context.py

import time
from states.storage import storage
from loader import bot


class FSMContext:

    def __init__(self, user_id: int):

        self.user_id = user_id

        storage.setdefault(
            user_id, {"state": None, "data": {}, "messages": [], "expires_at": None}
        )

    # ---------- STATE ----------

    async def set_state(self, state):
        storage[self.user_id]["state"] = state

    async def get_state(self):
        return storage[self.user_id]["state"]

    # ---------- TIMEOUT ----------

    async def set_timeout(self, seconds: int):
        storage[self.user_id]["expires_at"] = time.time() + seconds

    # ---------- DATA ----------

    async def get_data(self, key=None):
        data = storage[self.user_id]["data"]
        return data if key is None else data.get(key)

    async def update_data(self, **kwargs):
        storage[self.user_id]["data"].update(kwargs)

    # ---------- LIST ----------

    async def append(self, key, value):
        storage[self.user_id]["data"].setdefault(key, []).append(value)

    # ---------- DICT ----------

    async def dict_add(self, key, dict_key, value):
        storage[self.user_id]["data"].setdefault(key, {})[dict_key] = value

    # ---------- MESSAGES ----------

    async def add_message(self, message):

        mid = message.model_dump().get("mid")

        if mid:
            storage[self.user_id]["messages"].append(mid)

    async def delete_messages(self):

        for mid in storage[self.user_id]["messages"]:
            try:
                await bot.delete_message(message_id=mid)
            except Exception:
                ...

    # ---------- FINISH ----------

    async def finish(self):

        await self.delete_messages()

        storage.pop(self.user_id, None)
