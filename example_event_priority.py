import logging

from Akatosh import event, mundus


@event(at=0, priority=2, label="AuPost")
def au_post():
    print(f"{mundus.now}:\tAuPost deliver!")


@event(at=0, priority=1, label="StarTrek")
def star_trek():
    print(f"{mundus.now}:\tStar Trek deliver!")


mundus.set_logger(logging.DEBUG)
mundus.simulate()
