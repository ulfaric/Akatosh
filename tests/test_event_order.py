import asyncio
import logging
from math import inf
import time
import unittest
import akatosh
from akatosh.event import Event
from akatosh.universe import Mundus


class TestEventAfterEvent(unittest.TestCase):

    def setUp(self):
        self.watchdog_called = False
        self.hello_called = False
        self.world_called = False

    def watchdog(self):
        self.watchdog_called = True
        print(f"Watchdog at {Mundus.time}!")

    def hello_callback(self):
        self.hello_called = True
        print(f"Hello at {Mundus.time}")

    def world_callback(self):
        self.world_called = True
        print(f"World at {Mundus.time}")

    def test_events(self):
        hello = Event(0, 5, self.hello_callback, 0.005, watchdog=self.watchdog)
        world = Event(hello, inf, self.world_callback, 0.005)

        Mundus.enable_realtime()
        akatosh.logger.setLevel(logging.INFO)

        async def run_simulation():
            await asyncio.gather(Mundus.simulate(10))

        asyncio.run(run_simulation())

        self.assertTrue(self.hello_called, "Hello event was not called")
        self.assertTrue(self.world_called, "World event was not called")
        self.assertTrue(self.watchdog_called, "Watchdog was not called")


if __name__ == "__main__":
    unittest.main()
