import asyncio
import logging

from Akatosh import event, Mundus, InstantEvent


def hellow_world():
    print(f"{Mundus.now}:\tHello World!")


e = InstantEvent(at=5, action=hellow_world, label="Hello World")


@event(at=0, precursor=e, label="Hello World Again")
async def hellow_world_again():
    print(f"{Mundus.now}:\tHello World! Again!")


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
