from Akatosh.entity import Entity
from Akatosh.universe import Mundus

entity1 = Entity(1, 3, "Entity 1")
entity2 = Entity(entity1.termination, 4, "Entity 2")

Mundus.simulate(4)
