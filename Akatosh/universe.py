from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, List

from .states import State

from .logger import logger

if TYPE_CHECKING:
    from .event import Event


class Universe:
    def __init__(self) -> None:
        self._resolution = 1
        self._now: int | float = 0
        self._future_events: List[Event] = list()
        self._current_events: List[Event] = list()
        self._past_events: List[Event] = list()
        self._early_stop: bool = False
        self.set_logger(logging.ERROR)

    async def akatosh(self, till: int | float | None = None):
        while len(self.future_events) != 0:
            if self.early_stop:
                return

            if self.now < min(event.at for event in self.future_events):
                self._now = min(event.at for event in self.future_events)
                if till:
                    if self.now >= till:
                        return
                logger.debug(f"Time: {self.now}")

            for event in self.future_events:
                if event.at == self.now:
                    if event.state == State.ACTIVE:
                        logger.debug(f"Event {event.label} is triggered.")
                        self.future_events.remove(event)
                        self.current_events.append(event)
                    else:
                        if event.state == State.CANCELED:
                            logger.debug(f"Event {event.label} is canceled.")
                        else:
                            logger.debug(f"Event {event.label} is overdue.")
                        self.future_events.remove(event)
                        self.past_events.append(event)
                        event.state = State.ENDED
            self.current_events.sort(key=lambda event: event.priority)

            await asyncio.gather(*[actor._perform() for actor in self.current_events])

    def simulate(self, till: int | float | None = None):
        asyncio.run(self.akatosh(till))

    def set_logger(self, level: int):
        logger.setLevel(level)

    @property
    def resolution(self) -> int:
        return self._resolution

    @property
    def now(self) -> int | float:
        return self._now

    @property
    def future_events(self) -> List[Event]:
        return self._future_events

    @property
    def current_events(self) -> List[Event]:
        return self._current_events

    @property
    def past_events(self) -> List[Event]:
        return self._past_events

    @property
    def early_stop(self) -> bool:
        return self._early_stop

    @early_stop.setter
    def early_stop(self, value: bool):
        self._early_stop = value


mundus = Universe()
