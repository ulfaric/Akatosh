import logging

from Akatosh import InstantEvent, instant_event, Mundus


def hellow_world():
    print(f"{Mundus.now}:\tHello World!")


later_event = InstantEvent(at=5, action=hellow_world)


@instant_event(at=3, label="cancel")
def resume():
    print(f"{Mundus.now}:\tCancel future event.")
    later_event.cancel()


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
