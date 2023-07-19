```py
import logging

from Akatosh import Entity, Mundus, Resource, instant_event

# define a simple entity
class TestEntity(Entity):
    def on_creation(self):
        print(f"Entity {self.label} created")

    def on_termination(self):
        print(f"Entity {self.label} terminated")

# create first entity at 0s and terminate at 10s
test_entity_1 = TestEntity(label="Test Entity 1", create_at=0, terminate_at=10)

# create second entity at 0s and terminate at 12s but after first entity
test_entity_2 = TestEntity(label="Test Entity 2", create_at=0, terminate_at=12, precursor=test_entity_1)



Mundus.set_logger(logging.DEBUG)
Mundus.simulate()

print(test_entity_2.created_at, test_entity_2.terminated_at)

```
