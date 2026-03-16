import asyncio

from fsm_router import state_handler
from states.forms import Form
from loader import dp, bot
from loguru import logger


@state_handler("*")
async def any_state(event, state):

    logger.debug("сообщение внутри FSM")
    corrent_state = await state.get_state()
    await event.message.answer(f"{corrent_state}")
    
    
@state_handler(None)
async def no_state(event, state):

    logger.debug("пользователь без FSM")

    corrent_state = await state.get_state()
    await event.message.answer(f"{corrent_state}")