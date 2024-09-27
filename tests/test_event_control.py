import asyncio
import logging
import unittest
from Akatosh.event import Event
from Akatosh.universe import Mundus


class TestPauseEvent(unittest.TestCase):

    def test_pause_resume_event(self):
        Mundus.enable_realtime()
        Mundus.set_logging_level(logging.INFO)

        hello_world = Event(
            1,
            1.8,
            lambda: print(f"Hello World at {Mundus.time}"),
            priority=1,
            step=0.01,
        )
        pause = Event(1.2, 1.2, lambda: hello_world.pause())
        resume = Event(1.6, 1.6, lambda: hello_world.resume())

        async def run_simulation():
            await Mundus.simulate(2)

        asyncio.run(run_simulation())


if __name__ == "__main__":
    unittest.main()
