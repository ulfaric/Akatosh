import asyncio
import logging
import unittest
import akatosh
from akatosh.event import event
from akatosh.universe import Mundus


class TestEventPriority(unittest.TestCase):

    def setUp(self):
        self.event1_called = False
        self.event2_called = False

    def test_event_priority(self):
        Mundus.enable_realtime()
        akatosh.logger.setLevel(logging.INFO)

        @event(1, 1, label="Event 2", once=True, priority=2)
        def event2():
            self.event2_called = True
            print("World")

        @event(1, 1, label="Event 1", once=True, priority=1)
        def event1():
            self.event1_called = True
            print("Hello")

        asyncio.run(Mundus.simulate(1.1))

        self.assertTrue(self.event1_called, "Event 1 was not called")
        self.assertTrue(self.event2_called, "Event 2 was not called")


if __name__ == "__main__":
    unittest.main()
