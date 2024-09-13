import asyncio
from akatosh.entity import Entity
from akatosh.universe import Mundus

entity2 = Entity(1, 3, "Entity 2", 2)
entity1 = Entity(1, 3, "Entity 1", 1)

asyncio.run(Mundus.simulate(3))
