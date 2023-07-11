import random
from Akatosh import ContinuousEvent, Mundus
import logging


def action():
    print(f"Hello World at {Mundus.now} from Test 1")
    
def action2():
    print(f"Hello World at {Mundus.now} from Test 2")


event = ContinuousEvent(at=0, interval=random.random(), duration=10, action=action, label="Test")
event2 = ContinuousEvent(at=0, interval=random.random(), duration=15, action=action2, label="Test2", priority=-1, precursor=event)

# Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
