from Akatosh.entity import Entity
from Akatosh.universe import universe

entity2 = Entity(1,3,"Entity 2",2)
entity1 = Entity(1,3,"Entity 1",1)

universe.set_time_resolution(0)
universe.simulate(3)