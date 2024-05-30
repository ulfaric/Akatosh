import asyncio
import logging
import Akatosh
from Akatosh.event import Event
from Akatosh.universe import Mundus

hello = Event(0, 5, lambda: print(f"Hello at {Mundus.time}"))
world = Event(hello, 20, lambda: print(f"World at {Mundus.time}"),0.1)
pause = Event(at=10, till=10, action=lambda: Mundus.pause())

Mundus.enable_realtime()
Akatosh.logger.setLevel(logging.ERROR)
asyncio.run(Mundus.simulate(20))

