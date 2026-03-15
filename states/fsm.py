class State:

    def __init__(self):
        self.name = None
        self.group = None

    def __set_name__(self, owner, name):
        self.name = name
        self.group = owner

    def __repr__(self):
        return f"{self.group.__name__}:{self.name}" # type: ignore


class StatesGroupMeta(type):

    def __new__(mcs, name, bases, namespace):

        cls = super().__new__(mcs, name, bases, namespace)

        for key, value in namespace.items():
            if isinstance(value, State):
                value.name = key
                value.group = cls

        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    pass