# handlers/states.py
from fsm_router import state_handler
from states.forms import Form
from loguru import logger


@state_handler(Form.ONE)
async def one(event, state):

    logger.debug("мы зашли в state ONE")

    await state.set_state(Form.TWO)


@state_handler(Form.TWO)
async def two(event, state):

    logger.debug("мы зашли в state TWO")
