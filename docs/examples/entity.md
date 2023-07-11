```py
import logging

from Akatosh import Entity, Mundus, Resource, event

# define a simple test enity
class TestEntity(Entity):

    # implement the callback function upon creation
    def on_creation(self):
        print(f"Entity {self.label} created")

    # implement the callback function upon termination
    def on_termination(self):
        print(f"Entity {self.label} terminated")

# create the test entity
test_entity = TestEntity(label="Test Entity", create_at=0, terminate_at=10)

# create a simple resource
test_resource = Resource(label="Test Resource", capacity=1)

# create a simple  instant event to occupy the resource
@event(at=2, label="Test Event Get Resource")
def test_event():
    test_entity.get(test_resource, 1)

# enable debug message
Mundus.set_logger(logging.DEBUG)

# run the simulation
Mundus.simulate()
```