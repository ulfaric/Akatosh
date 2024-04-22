import logging
from Akatosh.entity import Entity
from Akatosh.event import Event, event
from Akatosh.resource import Resource
from Akatosh.universe import universe

res = Resource(100.0, 50.0)

user = Entity(0, 5, "User", priority=0)


@user.event(1.2, 4, "Use Resource", priority=0)
def user_event():
    if res.distribute(user, 1):
        print(f"Consumed {res.usage} resource.")
    else:
        print("Not enough resource")
        
@event(2.0,2.0)
def collect_resource():
    res.collect(user, 10)
        
@event(5.0,5.0)
def check_resource():
    print(f"Resource: {res.level}")

universe.time_resolution=1
universe.simulate(6)
