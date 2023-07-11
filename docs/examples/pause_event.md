```py
import logging

from Akatosh import InstantEvent, event, Mundus

# create a event that should occur at 5.0s
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")
later_event = InstantEvent(at=5, action=hellow_world)

# create a event to resume the later event.
@event(at=3, label="resume")
def resume():
    print(f"{Mundus.now}:\tResume the future event.")
    later_event.activate()

# create a event to pause the "later_event"
@event(at=0, label="pause")
def pause():
    print(f"{Mundus.now}:\tPause the future event.")
    later_event.deactivate()

# enable debug message
Mundus.set_logger(logging.DEBUG)

# run the simulation
Mundus.simulate()
```