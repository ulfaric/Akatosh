from Akatosh.entity import Entity
from Akatosh.event import event
from Akatosh.resource import Resource
from Akatosh.universe import Mundus

res = Resource(100.0, 50.0)

user = Entity(0, 5, "User", priority=0)


@user.event(1.2, 4, "Use Resource", priority=0)
def user_event():
    if res.distribute(user, 1):
        print(f"Consumed {res.usage} resource.")
    else:
        print("Not enough resource")


@event(2.0, 2.0)
def collect_resource():
    res.collect(user, 10)


@event(5.0, 5.0)
def check_resource():
    print(f"Resource: {res.level}")

Mundus.enable_realtime()
Mundus.time_resolution = 1
Mundus.simulate(6)
