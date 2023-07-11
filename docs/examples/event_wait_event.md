```py
import logging

from Akatosh import event, Mundus, InstantEvent

# define the actual function of the event
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

# create a instant event at simulation time 5s
e = InstantEvent(at=5, action=hellow_world, label="Hello World")

# create a instant event at simulation time 1s, but set the above event as precursor. 
# So this event will be triggered at 1s but not executed until above event is done.
@event(at=0, precursor=e, label="Hello World Again")
async def hellow_world_again():
    print(f"{Mundus.now}:\tHello World! Again!")

# enable debug message
Mundus.set_logger(logging.DEBUG)

# run the simulate
Mundus.simulate()

```