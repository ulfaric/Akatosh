import asyncio
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello_world = Event(1, 1.8, lambda: print("Hello World!"), priority=1)
pause = Event(1.2, 1.2, lambda: hello_world.pause())
resume = Event(1.6, 1.6, lambda: hello_world.resume())


asyncio.run(Mundus.simulate(2))
