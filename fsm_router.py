# fsm_router.py
handlers = {}


def state_handler(state):

    def wrapper(func):
        handlers[state] = func
        return func

    return wrapper