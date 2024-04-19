from __future__ import annotations

import asyncio
import logging
import time
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
        self._time_resolution = 3
        self._time_step = round(1 / pow(10, self.time_resolution), self.time_resolution)
        self._time = round(0.0 - self.time_step, self.time_resolution)
        self._realtime = False
        self._current_event_priority = 0
        self._max_event_priority = 0
        self._pending_events: List[Event] = list()

    def simulate(self, till: float):
        """Simulate the universe until the given time."""

        # Define the flow of time
        async def time_flow():
            """Flow of time."""
            simulation_start_time = time.time()
            while self.time < till:
                self._time += self.time_step
                self._time = round(self.time, self.time_resolution)
                logger.debug(f"Time:\t{self.time}")
                for event in self.pending_events:
                    asyncio.create_task(event())
                self.pending_events.clear()
                if self.realtime:
                    start_time = time.time()
                    # iterate through all event priorities
                    self._current_event_priority = 0
                    while self.current_event_priority <= self._max_event_priority:
                        logger.debug(f"Current Event Priority: {self.current_event_priority}")
                        await asyncio.sleep(0)
                        self._current_event_priority += 1
                    # wait for the time step
                    await universe.time_flow
                    end_time = time.time()
                    if end_time - start_time > self.time_step:
                        logger.warning(
                            f"Simulation time step exceeded real time by {round(((end_time - start_time - self.time_step)/self.time_step)*100,2)}%."
                        )
                else:
                    # iterate through all event priorities
                    self._current_event_priority = 0
                    while self.current_event_priority <= self._max_event_priority:
                        logger.debug(f"Current Event Priority: {self.current_event_priority}")
                        await asyncio.sleep(0)
                        self._current_event_priority += 1
                    # wait for the time step
                    await universe.time_flow
                    
            simulation_end_time = time.time()
            if self.realtime:
                logger.info(
                    f"Simulation completed in {round(simulation_end_time - simulation_start_time, 3)} seconds, exceeding real time by {round(((simulation_end_time - simulation_start_time - till)/till)*100,2)}%."
                )

        asyncio.run(time_flow())

    def enable_realtime(self, resolution: int = 1):
        if resolution < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        self.time_resolution = resolution
        self._time_step = 1 / pow(10, self.time_resolution)
        self._time = round(0.0 - self.time_step, self.time_resolution)
        self._realtime = True

    def set_logging_level(self, level: int = logging.DEBUG):
        logger.setLevel(level)

    def set_time_resolution(self, resolution: int):
        if resolution < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        self.time_resolution = resolution
        self._time_step = 1 / pow(10, self.time_resolution)
        self._time = round(0.0 - self.time_step, self.time_resolution)
        
    @property
    def time(self):
        return self._time

    @property
    def time_resolution(self):
        if self._time_resolution < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        return self._time_resolution

    @time_resolution.setter
    def time_resolution(self, value: int):
        if value < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        self._time_resolution = value
        self._time_step = 1 / pow(10, self.time_resolution)
        self._time = round(0.0 - self.time_step, self.time_resolution)

    @property
    def time_step(self):
        return self._time_step

    @property
    def realtime(self):
        return self._realtime

    @property
    def pending_events(self):
        return self._pending_events

    @property
    async def time_flow(self):
        if self.realtime == True:
            await asyncio.sleep(self.time_step)
        else:
            await asyncio.sleep(0)

    @property
    def current_event_priority(self):
        return self._current_event_priority
    
    @property
    def max_event_priority(self):
        return self._max_event_priority


universe = Universe()
