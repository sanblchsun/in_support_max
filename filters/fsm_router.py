# fsm_router.py

handlers = {}


def state_handler(*states):

    def wrapper(func):

        for state in states:
            handlers[state] = func

        return func

    return wrapper


async def dispatch(event, state):

    current = await state.get_state()

    # точное совпадение
    if current in handlers:
        return await handlers[current](event, state)

    # любое FSM состояние
    if current and "*" in handlers:
        return await handlers["*"](event, state)

    # без FSM
    if not current and None in handlers:
        return await handlers[None](event, state)
