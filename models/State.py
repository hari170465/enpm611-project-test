from enum import Enum


class State(str, Enum):
    """
    Whether issue is open or closed.
    """
    open = 'open'
    closed = 'closed'