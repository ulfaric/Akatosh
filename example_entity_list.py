import random
from Akatosh import Entity, EntityList, Mundus, State, logger

elist = EntityList([])

test_entity = Entity(label="test_entity", create_at=0, terminate_at=3)

elist.append(test_entity)


@test_entity.continuous_event(at=0, interval=1, duration=5, label="Test Entity List")
def test_action():
    print(f"{elist}")


Mundus.simulate()
