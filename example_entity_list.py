from Akatosh import Entity, EntityList, Mundus, State, logger

elist = EntityList([])

test_entity = Entity(label="test_entity", create_at=0, terminate_at=10)

elist.append(test_entity)


