# fsm_router.py

handlers = {}
any_state_handlers = []
no_state_handlers = []


def state_handler(state):
    """
    state может быть:
        конкретное состояние (Form.FIRMA)
        "*""  -> любое состояние
        None  -> отсутствие состояния
    """

    def wrapper(func):

        if state == "*":
            any_state_handlers.append(func)

        elif state is None:
            no_state_handlers.append(func)

        else:
            handlers[state] = func

        return func

    return wrapper