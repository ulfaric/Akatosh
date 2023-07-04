from dataclasses import dataclass
from http.client import CREATED
from multiprocessing.pool import TERMINATE
from tkinter.messagebox import CANCEL


@dataclass
class State:
    ENDED = "ENDED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELED = "CANCELED"
    CREATED = "CREATED"
    TERMINATED = "TERMINATED"
