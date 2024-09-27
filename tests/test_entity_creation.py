import asyncio
import logging
import unittest
from Akatosh.entity import Entity
from Akatosh.universe import Mundus


class TestEntityAfterEntity(unittest.TestCase):

    def test_entity_creation_after_termination(self):
        entity1 = Entity(1, 3, "Entity 1")
        entity2 = Entity(entity1.termination, 4, "Entity 2")

        Mundus.time_resolution = 1
        Mundus.enable_realtime()
        Mundus.set_logging_level(logging.ERROR)
        async def run_simulation():
            await Mundus.simulate(4)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
