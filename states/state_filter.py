from states.user_state import user_states


class StateFilter:

    def __init__(self, state):
        self.state = state

    async def __call__(self, event):
        user_id = event.message.sender.user_id
        return user_states.get(user_id) == self.state
