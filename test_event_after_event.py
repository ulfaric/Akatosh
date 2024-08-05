import asyncio
import logging
from math import inf
import time
import Akatosh
from Akatosh.event import Event
from Akatosh.universe import Mundus

def watchdog():
    print(f"Watchdog at {Mundus.time}!")

hello = Event(0,5,lambda: print(f"Hello at {Mundus.time}"), 0.0005, watchdog=watchdog)
world = Event(hello, inf, lambda: print(f"World at {Mundus.time}"),0.005)

async def pause_and_resume():
    await asyncio.sleep(2.5)
    Mundus.set_timescale(10)
    await asyncio.sleep(2.5)
    Mundus.set_timescale(1)

Mundus.enable_realtime()
Akatosh.logger.setLevel(logging.INFO)

async def main():
    await asyncio.gather(Mundus.simulate(inf), pause_and_resume())

asyncio.run(main())