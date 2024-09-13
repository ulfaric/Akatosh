import asyncio
import unittest
from akatosh.entity import Entity
from akatosh.universe import Mundus


class TestEntityPriority(unittest.TestCase):
    def test_entity_priority(self):
        entity2 = Entity(1, 3, "Entity 2", 2)
        entity1 = Entity(1, 3, "Entity 1", 1)

        async def run_simulation():
            await Mundus.simulate(4)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
