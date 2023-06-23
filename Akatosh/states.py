from dataclasses import dataclass
from tkinter.messagebox import CANCEL


@dataclass
class State:
    ENDED = -1
    ACTIVE = 0
    INACTIVE = 1
    CANCELED = 2
