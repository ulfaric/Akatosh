import asyncio
from Akatosh.event import event
from Akatosh.universe import Mundus


@event(1, 1, label = "Event 2", once=True, priority=2)
def event2():
    print("World")


@event(1, 1, label =  "Event 1", once=True, priority=1)
def event1():
    print("Hello")

Mundus.enable_realtime(1)
asyncio.run(Mundus.simulate(2))
