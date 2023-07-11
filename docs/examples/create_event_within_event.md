```py
import logging

from Akatosh import event, Mundus

# create a instant event at simulation time 1.0s
@event(at=1)
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

    # this instant event create anothe instant event at simulation time 5.0s
    @event(at=5)
    def hellow_world_again():
        print(f"{Mundus.now}:\tHello World! Again!")

# enable debug message
Mundus.set_logger(logging.DEBUG)

# simulate
Mundus.simulate()
```