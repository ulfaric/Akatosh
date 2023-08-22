import logging

from Akatosh import Entity, Mundus, Resource, instant_event

# define a simple entity
class TestEntity(Entity):
    def on_creation(self):
        print(f"Entity {self.label} created")

    def on_termination(self):
        print(f"Entity {self.label} terminated")

# create first entity at 0s and terminate at 10s
test_entity_1 = TestEntity(label="Test Entity 1", create_at=0, terminate_at=5)
test_entity_2 = TestEntity(label="Test Entity 2", create_at=0, terminate_at=6, precursor=[test_entity_1])

# create second entity at 0s and terminate at 12s but after first entity
test_entity_3 = TestEntity(label="Test Entity 3", create_at = 2, terminate_at=7, precursor=[test_entity_1, test_entity_2])



Mundus.set_logger(logging.DEBUG)
Mundus.simulate()

print(test_entity_3.created_at, test_entity_3.terminated_at)