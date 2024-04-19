import asyncio
from math import inf
from Akatosh.universe import universe
from Akatosh.resource import Resource
from Akatosh.entity import Entity
from Akatosh.event import event, Event

res = Resource(100.0, 50.0)
lock = Event(0.9,0.9, lambda: print("Unlocked!"))

user = Entity(lock, 1.1, "User")

@user.event(1.2,1.2, "Use Resource")
def user_event():
    if res.distribute(user, 1):
        print(res.level)
    else:
        print("Not enough resource")



universe.simulate(1.2)
