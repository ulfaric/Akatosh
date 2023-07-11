```py
import random
from Akatosh import ContinuousEvent, Mundus
import logging

# define the actual function for continuous event
def action():
    print(f"Hello World at {Mundus.now}")

# create the continuous event
event = ContinuousEvent(at=0, interval=random.random(), duration=10, action=action)

Mundus.set_logger(logging.DEBUG)
Mundus.simulate()

```