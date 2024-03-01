from __future__ import annotations

from enum import Enum
import inspect
from math import log
from typing import Any, Callable, List
from uuid import uuid4

from . import EventState, logger
from .universe import Mundus


class Event:

    def __init__(
        self,
        at: int | float | Callable[..., int] | Callable[..., float],
        after: List[Event] | None = None,
        action: Callable | None = None,
        priority: int | float | Callable[..., int] | Callable[..., float] = 0,
        state: EventState = EventState.Future,
        label: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._id = uuid4().hex
        self._at = at if not callable(at) else round(at(), Mundus.resolution)
        self._after = after
        self._action = action
        self._priority = priority if not callable(priority) else priority()
        self._state = state
        self._label = label
        self._args = args
        self._kwargs = kwargs
        self._followers: List[Event] = list()
        
        if self.after is None:
            Mundus.future_events.append(self)
        else:
            for event in self.after:
                event.followers.append(self)


    async def __call__(self) -> Any:
        if self.state == EventState.Current:
            if self.action:
                if inspect.iscoroutinefunction(self.action):
                    await self.action(*self._args, **self._kwargs)
                else:
                    self.action(*self._args, **self._kwargs)
            self._state = EventState.Past
            Mundus.current_events.remove(self)
            Mundus.past_events.append(self)
            logger.debug(f"Event: {self.label} is executed.")
            for event in self.followers:
                if event.after:
                    if all([follower.state == EventState.Past for follower in event.after]):
                        event._at = Mundus.now
                        Mundus.future_events.append(event)
                        logger.debug(f"Follow-up event {event.label} is added to the future events queue.")
                    else:
                        continue
                else:
                    logger.error(f"Event {event.label} is a follow up event but has no waiting events.")
        else:
            logger.error(f"Event {self.label} is not in the current state.")

    def __str__(self) -> str:
        return f"Event: {self.label}, at: {self.at}, state: {self.state}"

    def cancel(self) -> None:
        """Cancel the event."""
        self._state = EventState.Past

    @property
    def id(self) -> str:
        return self._id

    @property
    def at(self) -> int | float:
        return self._at

    @property
    def after(self) -> List[Event] | None:
        return self._after
    
    @property
    def followers(self) -> List[Event]:
        return self._followers

    @property
    def action(self) -> Callable | None:
        return self._action

    @property
    def priority(self) -> int | float:
        return self._priority

    @property
    def state(self) -> EventState:
        return self._state

    @property
    def label(self) -> str | None:
        return self._label


def event(
    at: int | float | Callable[..., int] | Callable[..., float],
    priority: int | float | Callable[..., int] | Callable[..., float] = 0,
    label: str | None = None,
    state: EventState = EventState.Future,
    *args: Any,
    **kwargs: Any,
):
    def _event(func: Callable):
        return Event(
            at=at,
            action=func,
            priority=priority,
            label=label,
            state=state,
            *args,
            **kwargs,
        )

    return _event
