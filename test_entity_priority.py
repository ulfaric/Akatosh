import asyncio
from Akatosh.entity import Entity
from Akatosh.universe import Mundus

entity2 = Entity(1, 3, "Entity 2", 2)
entity1 = Entity(1, 3, "Entity 1", 1)

asyncio.run(Mundus.simulate(3))
