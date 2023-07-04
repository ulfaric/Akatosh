import random
from Akatosh import ContinousEvent, Mundus
import logging


def action():
    print(f"Hello World at {Mundus.now}")


event = ContinousEvent(at=0, interval=random.random(), duration=10, action=action)
Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
