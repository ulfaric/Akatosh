import asyncio
import logging
import unittest
from akatosh.event import Event
from akatosh.universe import Mundus


class TestCancelEvent(unittest.TestCase):

    def test_event_cancellation(self):

        # Mundus.enable_realtime()
        Mundus.set_logging_level(logging.INFO)

        hello_world = Event(1, 1.5, lambda: print(f"Hello World at {Mundus.time}!"), priority=0, step=0.1)
        cancel = Event(1.3, 1.3, lambda: hello_world.cancel(), priority=1)
        greet_world = Event(hello_world, 2, lambda: print(f"Greetings World at {Mundus.time}!"), priority=1)

        async def run_simulation():
            await Mundus.simulate(2)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
