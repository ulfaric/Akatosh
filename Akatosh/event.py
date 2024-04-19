from __future__ import annotations
import asyncio
from typing import Any, Callable, Optional
from . import logger
from .universe import universe


class Event:

    def __init__(
        self,
        at: float | Event,
        till: float | Event,
        action: Callable,
        label: Optional[str] = None,
        once: bool = False,
        priority: int = 0,
    ) -> None:
        if universe.time >= at:
            raise ValueError(f"Event can only be scheduled for the future.")
        self._at = at
        self._till = till
        self._action = action
        self._started = False
        self._acted = False
        self._ended = False
        self._paused = False
        self._label = label
        self._once = once
        self._priority = priority
        universe.pending_events.append(self)
        if self.priority > universe.max_event_priority:
            universe._max_event_priority = self.priority

    async def __call__(self) -> Any:
        while True:

            if self.ended == True:
                return

            while True:
                if self.priority == universe.current_event_priority:
                    break
                else:
                    await asyncio.sleep(0)

            if self.started == False:
                if isinstance(self.at, Event):
                    if self.at.ended == True:
                        self._started = True
                        logger.debug(f"Event {self} started.")
                else:
                    if self.at <= universe.time:
                        self._started = True
                        logger.debug(f"Event {self} started.")

            if self.started == True and self.ended == False and self.paused == False:
                if asyncio.iscoroutinefunction(self._action):
                    await self._action()
                else:
                    self._action()
                self._acted = True
                logger.debug(f"Event {self} acted.")
                if self._once == True:
                    self._ended = True
                    logger.debug(f"Event {self} ended.")
                    return

            if self.ended == False:
                if isinstance(self.till, Event):
                    if self.till.ended == True:
                        self._ended = True
                        logger.debug(f"Event {self} ended.")
                        return
                else:
                    if self.till <= universe.time:
                        self._ended = True
                        logger.debug(f"Event {self} ended.")
                        return

            await universe.time_flow

    def __str__(self) -> str:
        if self.label is None:
            return f"Event {id(self)}"
        return self.label

    def cancel(self):
        self._ended = True
        logger.debug(f"Event {self} cancelled.")

    def pause(self):
        self._paused = True
        logger.debug(f"Event {self} paused.")

    def resume(self):
        self._paused = False
        logger.debug(f"Event {self} resumed.")

    @property
    def at(self):
        return self._at

    @property
    def till(self):
        return self._till

    @property
    def started(self):
        return self._started

    @property
    def ended(self):
        return self._ended

    @property
    def paused(self):
        return self._paused

    @property
    def label(self):
        return self._label

    @property
    def once(self):
        return self._once

    @property
    def priority(self):
        return self._priority


def event(
    at: float | Event,
    till: float | Event,
    label: Optional[str] = None,
    once: bool = False,
    priority: int = 0,
):
    def _event(action: Callable) -> Event:
        return Event(at, till, action, label, once, priority)

    return _event
