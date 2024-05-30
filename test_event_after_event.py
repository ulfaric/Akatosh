import asyncio
import logging
import Akatosh
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello = Event(0, 5, lambda: print(f"Hello at {Mundus.time}"))
world = Event(hello, 10, lambda: print(f"World at {Mundus.time}"),1)

Mundus.enable_realtime(time_scale=1)
Akatosh.logger.setLevel(logging.ERROR)
asyncio.run(Mundus.simulate(10))
