```py
import logging
from Akatosh import Entity, EntityList, Mundus

# create an entity list
elist = EntityList([])

# create an test entity
test_entity = Entity(label="test_entity", create_at=0, terminate_at=3)

# test entity engage an instant event that append itself to the entity list
@test_entity.instant_event(at=2, label="Append Entity List")
def action2():
    elist.append(test_entity)

# test entity engage an continuous event that print the entity list
@test_entity.continuous_event(at=1, interval=1, duration=5, label="Test Entity List - Continuous")
def test_action():
    print(f"{elist}")

# enable the debug message
Mundus.set_logger(logging.DEBUG)

# run the simulation
Mundus.simulate()
```