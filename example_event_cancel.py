import logging

from Akatosh import InstantEvent, event, mundus


def hellow_world():
    print(f"{mundus.now}:\tHello World!")


later_event = InstantEvent(at=5, action=hellow_world)


@event(at=3, label="cancel")
def resume():
    print(f"{mundus.now}:\tCancel future event.")
    later_event.cancel()


mundus.set_logger(logging.DEBUG)
mundus.simulate()
