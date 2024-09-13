import asyncio
import logging
import unittest
from akatosh.event import event
from akatosh.universe import Mundus
from akatosh import logger


class TestContinuousEvent(unittest.TestCase):

    def test_hello_world_event(self):
        @event(at=0, till=0.5, step=0.001)
        def hello_world():
            print(f"Hello World at {Mundus.time}!")

        Mundus.set_logging_level(logging.INFO)
        Mundus.enable_realtime()

        async def run_simulation():
            await Mundus.simulate(0.5)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
