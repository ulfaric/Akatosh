import logging
from Akatosh.entity import Entity
from Akatosh.event import Event, event
from Akatosh.resource import Resource
from Akatosh.universe import universe

res = Resource(100.0, 50.0)
lock = Event(0.9,0.9, lambda: print("Unlocked!"))

user = Entity(lock, 5, "User")

@user.event(1.2,4, "Use Resource")
def user_event():
    if res.distribute(user, 1):
        print(res.level)
    else:
        print("Not enough resource")


universe.enable_realtime()
universe.set_logging_level(logging.INFO)
universe.simulate(10)
