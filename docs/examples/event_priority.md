```py
import logging

from Akatosh import event, Mundus

# create a event with priority 2
@event(at=0, priority=2, label="AuPost")
def au_post():
    print(f"{Mundus.now}:\tAuPost deliver!")

# create a event with priority 1
@event(at=0, priority=1, label="StarTrek")
def star_trek():
    print(f"{Mundus.now}:\tStar Trek deliver!")


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
# the Star Trek will deliver first, AuPost sucks!
```