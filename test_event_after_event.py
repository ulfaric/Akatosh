import asyncio
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello = Event(0.5, 0.5, lambda: print("Hello"))
world = Event(hello, 0.5, lambda: print("World"))

Mundus.enable_realtime()
asyncio.run(Mundus.simulate(1))
