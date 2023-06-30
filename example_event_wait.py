import asyncio
import logging

from Akatosh import event, mundus, InstantEvent


def hellow_world():
    print(f"{mundus.now}:\tHello World!")


e = InstantEvent(at=5, action=hellow_world, label="Hello World")


@event(at=7, precursor=e, label="Hello World Again")
def hellow_world_again():
    print(f"{mundus.now}:\tHello World! Again!")


mundus.set_logger(logging.DEBUG)
mundus.simulate()
