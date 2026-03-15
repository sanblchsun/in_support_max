from states.context import FSMContext
from loguru import logger


class StateFilter:

    def __init__(self, *states):
        self.states = {f"{s.group.__name__}:{s.name}" for s in states}

    async def __call__(self, event, state: FSMContext) -> bool:

        logger.debug("Мы попали в StateFilter УРА!")

        if not state:
            return False

        current = await state.get_state()

        return current in self.states
