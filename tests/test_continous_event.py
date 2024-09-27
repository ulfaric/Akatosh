import asyncio
import logging
import unittest
from Akatosh.event import event
from Akatosh.universe import Mundus
from Akatosh import logger


class TestContinuousEvent(unittest.TestCase):

    def test_hello_world_event(self):
        @event(at=0, till=0.5)
        def hello_world():
            print(f"Hello World at {Mundus.time}!")

        Mundus.set_logging_level(logging.INFO)
        Mundus.enable_realtime()

        async def run_simulation():
            await Mundus.simulate(0.5)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
