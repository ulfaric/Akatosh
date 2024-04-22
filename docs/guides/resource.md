# Resource

`Resource` can be distributed to `Entity` or collect from them. It has a capacity for overall amount can be stored, a current level for the overall amount left and a usage for overall amount has been disyributed. `Resource` tracks the usage per `Entity`. When a `Entity` is terminated, its occupied resource will be automatically released.

To distribute `Resource` to `Entity`, you could use either `distribute()` class function from `Resource` or `acquire()` class function from `Entity`. Note that if the required amount is larger than the current level of the resource, all remaining available amount will be given to the enity.

Similar, to return/collect resource, you could user `collect()` class function from `Resource` or `release()` class function from `Entity`. If the amount is larger than the current occupied amount by the user, all occupied resource will be released/collected.

```py
from Akatosh.entity import Entity
from Akatosh.event import event
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
```
