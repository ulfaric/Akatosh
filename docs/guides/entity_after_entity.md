# Entity after entity

The following codes create two entities that the second entity will be created after the first entity's termination.

```py
from Akatosh.entity import Entity
from Akatosh.universe import universe

entity1 = Entity(1,3,"Entity 1")
entity2 = Entity(entity1.termination,4,"Entity 2")

universe.set_time_resolution(0)
universe.simulate(4)

```