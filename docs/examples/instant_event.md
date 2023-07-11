```py
import logging

from Akatosh import event, Mundus

# create an instant event at simulation time 5.0s, print "Hello World Again!"
@event(at=5)
def hellow_world_again():
    print(f"{Mundus.now}:\tHello World! Again!")

# create an instant event at simulation time 1.0s, print "Hello World!"
@event(at=1)
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

# enable debug message
Mundus.set_logger(logging.DEBUG)

# simulate
Mundus.simulate()
```