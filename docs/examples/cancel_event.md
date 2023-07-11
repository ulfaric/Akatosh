```py
import logging

from Akatosh import InstantEvent, event, Mundus

# define the event function
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

# create a event occurs at 5s
later_event = InstantEvent(at=5, action=hellow_world)

# create a event  occurs at 3s to cancel the above event at 5s
@event(at=3, label="cancel")
def resume():
    print(f"{Mundus.now}:\tCancel future event.")
    later_event.cancel()

# enable debug message
Mundus.set_logger(logging.DEBUG)

# run the simulation
Mundus.simulate()
```