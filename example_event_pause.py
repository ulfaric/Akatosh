import logging

from Akatosh import InstantEvent, instant_event, Mundus


def hellow_world():
    print(f"{Mundus.now}:\tHello World!")


later_event = InstantEvent(at=5, action=hellow_world)


# @event(at=3, label="resume")
# def resume():
#     print(f"{Mundus.now}:\tResume previous event.")
#     later_event.activate()


@instant_event(at=0, label="pause")
def pause():
    print(f"{Mundus.now}:\tPause the future event.")
    later_event.deactivate()


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
