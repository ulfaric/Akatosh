import asyncio
import logging
import akatosh
from akatosh.event import event
from akatosh.universe import Mundus


@event(1, 1, label = "Event 2", once=True, priority=2)
def event2():
    print("World")


@event(1, 1, label =  "Event 1", once=True, priority=1)
def event1():
    print("Hello")

Mundus.enable_realtime()
akatosh.logger.setLevel(logging.INFO)
asyncio.run(Mundus.simulate(1.1))
