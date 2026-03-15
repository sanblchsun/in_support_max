# handlers/states.py
from fsm_router import state_handler
from states.forms import Form
from loguru import logger


@state_handler(Form.BEGINNING)
async def one(event, state):

    logger.debug("мы зашли в state BEGINNING")

    await state.set_state(Form.FIRMA)


@state_handler(Form.FIRMA)
async def two(event, state):

    logger.debug("мы зашли в state FIRMA")
