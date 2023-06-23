import logging

from Akatosh import Event, event, mundus


def hellow_world():
    print(f"{mundus.now}:\tHello World!")


later_event = Event(at=5, action=hellow_world)


@event(at=3, label="resume")
def resume():
    print(f"{mundus.now}:\tResume previous event.")
    later_event.activate()


@event(at=0, label="pause")
def pause():
    print(f"{mundus.now}:\tPause the future event.")
    later_event.deactivate()


mundus.set_logger(logging.DEBUG)
mundus.simulate()
