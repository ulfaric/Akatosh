import asyncio
import logging
import unittest
from Akatosh.event import event
from Akatosh.universe import Mundus


class TestEventCreateEvent(unittest.TestCase):

    def test_hello_world_event(self):
        @event(0.5, 0.5)
        def hello():
            print("Hello")

            @event(0.6, 0.6)  # new event must be after the current event
            def world():
                print("World")

        async def run_simulation():
            Mundus.enable_realtime()
            Mundus.set_logging_level(logging.INFO)
            await Mundus.simulate(1)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
