# Entity

In Akatosh, an Entity is an object that can engage events during its life-cycle like a NPC. The NPC like in games, can "do different things" and "these things" stop happening when the NPC is died.

## Create an Entity

Entity can be created similar to an event:

```py
from Akatosh.entity import Entity
from Akatosh.universe import universe

entity = Entity(1,3,"Entity") 
universe.simulate(4)
```

However, upon creation of a entity, two instant events are created: creation & termination, which determine the life cycle of the entity. These two events can be accessed as:

```py
entity.creation
entity.termination
```

## Create an Entity after an event

Similar to event, you can define the creation time of an entity based on an event:

```py
from Akatosh.entity import Entity
from Akatosh.universe import universe

entity = Entity(1,3,"Entity") 
entity2 = Entity(entity.termination, 4, "Second Entity") # entity 2 will be created after the first entity is terminated.
universe.simulate(4)
```

## Engage a event

Akatosh gives a decorator to allow entity to engage an event. The engaged event will be assoicated with the entity. If a continous entity is engaged, it will be cancelled if the entity is terminated but the event is not ended. If a instant event is engaged but the entity terminated before it starts, the event will also be cancelled.

```py
@entity.event(2,2,"Hello World")
def hello_world():
    print("Hello World!")
```
