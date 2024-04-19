from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List

from . import logger

if TYPE_CHECKING:
    from .event import Event


class Universe:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._time_resolution = 2
        self._time_step = 1 / pow(10, self.time_resolution)
        self._time = round(0.0 - self.time_step, self.time_resolution)

        self._pending_events: List[Event] = list()

    def simulate(self, till: float):
        """Simulate the universe until the given time."""

        # Define the flow of time
        async def time_flow():
            """Flow of time."""
            while self.time < till:
                self._time += self.time_step
                self._time = round(self.time, self.time_resolution)
                logger.debug(f"Time:\t{self.time}")
                for event in self.pending_events:
                        asyncio.create_task(event())
                self.pending_events.clear()
                await asyncio.sleep(0)

        asyncio.run(time_flow())

    @property
    def time(self):
        return self._time

    @property
    def time_resolution(self):
        return self._time_resolution

    @property
    def time_step(self):
        return self._time_step

    @property
    def pending_events(self):
        return self._pending_events
    
    @property
    async def time_flow(self):
        await asyncio.sleep(0)


universe = Universe()
