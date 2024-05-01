import asyncio
from Akatosh.event import event
from Akatosh.universe import Mundus


@event(0.5, 0.5)
def hello():
    print("Hello")

    @event(0.6, 0.6)  # new event must be after the current event
    def world():
        print("World")


asyncio.run(Mundus.simulate(1))
