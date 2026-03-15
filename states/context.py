# states/context.py
import asyncio
from states.storage import storage
from states.timeout_tasks import timeout_tasks


class FSMContext:

    def __init__(self, chat_id: int, user_id: int, bot):

        self.chat_id = chat_id
        self.user_id = user_id
        self.bot = bot
        self.key = (chat_id, user_id)

        storage.setdefault(self.key, {"state": None, "data": {}, "messages": []})

    # ---------- STATE ----------
    async def set_state(self, state):
        storage[self.key]["state"] = state

    async def get_state(self):
        return storage[self.key]["state"]

    # ---------- TIMEOUT ----------

    async def set_timeout(self, seconds: int):

        if self.key in timeout_tasks:
            timeout_tasks[self.key].cancel()

        timeout_tasks[self.key] = asyncio.create_task(self._timeout(seconds))

    async def _timeout(self, seconds: int):

        await asyncio.sleep(seconds)

        try:

            await self.bot.send_message(
                chat_id=self.chat_id,
                text="⏰ Ваша заявка отменена из-за истечения времени. Нажмите /start.",
            )

        except Exception:
            ...

        await self.finish()

    # ---------- DATA ----------
    async def update_data(self, **kwargs):
        storage[self.key]["data"].update(kwargs)

    async def get_data(self, key=None):
        data = storage[self.key]["data"]
        return data if key is None else data.get(key)

    async def append(self, key, value):
        storage[self.key]["data"].setdefault(key, []).append(value)

    async def dict_add(self, key, dict_key, value):
        storage[self.key]["data"].setdefault(key, {})[dict_key] = value

    async def clear(self):
        storage.pop(self.key, None)

    # ---------- MESSAGES ----------

    async def add_message(self, message):

        mid = message.model_dump().get("message").get("body").get("mid")

        if mid:
            storage[self.key]["messages"].append(mid)

    async def delete_messages(self):

        for mid in storage[self.key]["messages"]:
            try:
                await self.bot.delete_message(message_id=mid)
            except Exception:
                ...

    # ---------- FINISH ----------

    async def finish(self):

        await self.delete_messages()

        if self.key in timeout_tasks:
            timeout_tasks[self.key].cancel()
            timeout_tasks.pop(self.key)

        storage.pop(self.key, None)
