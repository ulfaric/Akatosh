import asyncio
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello_world = Event(1, 1.5, lambda: print("Hello World!"), priority=2)
cancel = Event(1.3, 1.3, lambda: hello_world.cancel(), priority=1)

Mundus.time_resolution = 2
asyncio.run(Mundus.simulate(2))
