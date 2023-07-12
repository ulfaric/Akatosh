import logging

from Akatosh import instant_event, Mundus


@instant_event(at=0, priority=2, label="AuPost")
def au_post():
    print(f"{Mundus.now}:\tAuPost deliver!")


@instant_event(at=0, priority=1, label="StarTrek")
def star_trek():
    print(f"{Mundus.now}:\tStar Trek deliver!")


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
