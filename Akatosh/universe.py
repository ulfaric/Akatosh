from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List

from . import logger, EventState

if TYPE_CHECKING:
    from .event import Event


class Universe:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Universe, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """The Simulation Universe."""
        self._resolution = (
            3  # the resolution of the time. 1 means minimum time unit is 0.1 second.
        )
        self._now: int | float = -1  # the current time of the simulated universe.
        self._future_events: List[Event] = list()  # the future events queue.
        self._current_events: List[Event] = list()  # the current events queue.
        self._past_events: List[Event] = list()  # the past events queue.
        self._alduin: bool = False  # trigger to stop the simulation.

    async def akatosh(self, till: int | float | None = None):
        while len(self.future_events) != 0:

            # stop the simulation if the trigger is set.
            if self.alduin:
                return

            # stop the simulation if the time is up.
            if till:
                if self.now >= till:
                    return
            logger.debug(f"Current Time: {self.now}")
            logger.debug(
                f"Future Events:\n"
                + "\n".join(["\t" + str(event) for event in self.future_events])
            )
            
            # sort future events by time.
            self.future_events.sort(key=lambda event: event.at)
            
            # update the current time step.
            if self.now < self.future_events[0].at:
                self._now = self.future_events[0].at
            logger.debug(f"Current Time Step to: {self.now}")
            
            # update the current events queue.
            for event in self.future_events:
                self.current_events.append(event)

            # sort current events by priority.
            self.current_events.sort(key=lambda event: event.priority)
            while len(self.current_events) != 0:
                current_priority = self.current_events[0].priority
                logger.debug(f"Current Priority: {current_priority}")
                events_to_execute = list()
                for event in self.current_events:
                    if event.priority == current_priority:
                        event._state = EventState.Current
                        events_to_execute.append(event)
                        self.future_events.remove(event)
                logger.debug(
                    f"Events to Execute:\n"
                    + "\n".join(["\t" + str(event) for event in events_to_execute])
                )
                await asyncio.gather(*[event() for event in events_to_execute])

    def simulate(self, till: int | float | None = None):
        """Start the simulation."""
        asyncio.run(self.akatosh(till))

    @property
    def resolution(self) -> int:
        """Return  the resolution of the time."""
        return self._resolution

    @resolution.setter
    def resolution(self, value: int):
        """Set the resolution of the time."""
        if value <= 0:
            raise ValueError("Resolution must be greater than 0.")
        self._resolution = value

    @property
    def now(self) -> int | float:
        """Return the current time of the simulated universe."""
        return self._now

    @property
    def future_events(self) -> List[Event]:
        """Return the future events queue."""
        return self._future_events

    @property
    def current_events(self) -> List[Event]:
        """Return the current events queue."""
        return self._current_events

    @property
    def past_events(self) -> List[Event]:
        """Return the past events queue."""
        return self._past_events

    @property
    def alduin(self) -> bool:
        """Return the trigger to stop the simulation."""
        return self._alduin

    @alduin.setter
    def alduin(self, value: bool):
        """Set the trigger to stop the simulation."""
        self._alduin = value


Mundus = Universe()
