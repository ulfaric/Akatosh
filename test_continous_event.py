import asyncio
import logging
from Akatosh.event import event
from Akatosh.universe import Mundus
from Akatosh import logger


@event(at = 1, till = 1.5)
def hello_world():
    print(f"Hello World at {Mundus.time}!")


logger.setLevel(logging.ERROR)
Mundus.enable_realtime()
asyncio.run(Mundus.simulate(2))
