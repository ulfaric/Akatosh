from cgi import test
import logging

from Akatosh import Entity, Mundus, Resource, event


class TestEntity(Entity):
    def on_creation(self):
        print(f"Entity {self.label} created")

    def on_termination(self):
        print(f"Entity {self.label} terminated")


test_entity = TestEntity(label="Test Entity", create_at=0, terminate_at=10)

test_resource = Resource(label="Test Resource", capacity=1)

@event(at=2, label="Test Event Get Resource")
def test_event():
    test_entity.get(test_resource, 1)


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
