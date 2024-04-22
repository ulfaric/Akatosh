import logging
from Akatosh.event import event
from Akatosh.universe import Mundus


@event(1, 1.5)
def hello_world():
    print(f"Hello World at {Mundus.time}!")


@event(1, 1.5)
def hello_world2():
    print(f"Hello World at {Mundus.time}!")


Mundus.enable_realtime()
Mundus.simulate(2)
