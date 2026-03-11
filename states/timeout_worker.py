# fsm_timeout_worker.py

import asyncio
import time
import logging

from states.storage import storage
from states.context import FSMContext
from loader import bot


async def fsm_timeout_worker():

    while True:

        now = time.time()

        for user_id, user_data in list(storage.items()):

            expires_at = user_data.get("expires_at")

            if not expires_at:
                continue

            if now >= expires_at:

                state = FSMContext(user_id)

                try:

                    await bot.send_message(
                        user_id=user_id,
                        text="⏰ Ваша заявка отменена из-за истечения времени. Нажмите /start."
                    )

                except Exception:
                    ...

                await state.finish()

                logging.info(f"FSM timeout user {user_id}")

        await asyncio.sleep(5)