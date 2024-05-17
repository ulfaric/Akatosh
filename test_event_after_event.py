import asyncio
import logging
import Akatosh
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello = Event(0, 5, lambda: print(f"Hello at {Mundus.time}"))
world = Event(hello, 10, lambda: print(f"World at {Mundus.time}"))

Mundus.enable_realtime()
Akatosh.logger.setLevel(logging.DEBUG)
asyncio.run(Mundus.simulate(10))
