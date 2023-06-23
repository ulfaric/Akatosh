from __future__ import annotations

from math import inf
from typing import Callable, List

from .states import State
from .universe import mundus
from .logger import logger


class Event:
    def __init__(
        self,
        at: int | float | Callable,
        precursor: Event | List[Event] | None = None,
        action: Callable | None = None,
        priority: int | float | Callable = 0,
        label: str | None = None,
        **kwargs,
    ) -> None:
        # set the time
        if callable(at):
            self._at = round(at(), mundus.resolution)
        else:
            self._at = round(at, mundus.resolution)
        # set the target event(s) that this event should wait and follow
        if isinstance(precursor, list):
            self._precursor = precursor
        else:
            self._precursor = [precursor] if precursor is not None else []
        self._follower: List[Event] = []
        for event in self.precursor:
            event._follower.append(self)
        # set the state
        if precursor:
            self.state = State.INACTIVE
        else:
            self.state = State.ACTIVE
        # set the action and the priority
        if action:
            self._action = action
        if callable(priority):
            self._priority = priority()
        else:
            self._priority = priority
        # assign label
        self._label = label
        # add to the universe
        mundus.future_events.append(self)

    def _end(self):
        self.state = State.ENDED
        for event in self.follower:
            try:
                event.activate()
            except RuntimeError:
                logger.debug(f"Event {event.label} passed due time.")

    def activate(self, force: bool = False):
        if self.ended:
            raise RuntimeError(f"Event {self.label} has already ended.")

        if force:
            self.state = State.ACTIVE
            logger.debug(f"Event {self.label} is set to active.")
        else:
            if all(e.state == State.ENDED for e in self.precursor):
                self.state = State.ACTIVE
                logger.debug(f"Event {self.label} is set to active.")
            else:
                raise RuntimeError(
                    f"Event {self.label} is waiting for other events to end."
                )

    def deactivate(self):
        if self.ended:
            raise RuntimeError(f"Event {self.label} has already ended.")
        self.state = State.INACTIVE

    def cancel(self):
        if self.ended:
            raise RuntimeError(f"Event {self.label} has already ended.")
        self.state = State.CANCELED

    async def _perform(self):
        if self.action:
            self.action()
        mundus.current_events.remove(self)
        mundus.past_events.append(self)
        self._end()
        logger.debug(f"Event {self.label} is ended.")

    @property
    def label(self) -> str | None:
        return self._label

    @property
    def at(self) -> int | float:
        return self._at

    @property
    def precursor(self) -> List[Event]:
        return self._precursor

    @property
    def follower(self) -> List[Event]:
        return self._follower

    @property
    def action(self) -> Callable | None:
        return self._action

    @property
    def priority(self) -> int | float:
        return self._priority

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, state: int):
        self._state = state

    @property
    def active(self) -> bool:
        return State.ACTIVE == self.state

    @property
    def inactive(self) -> bool:
        return State.INACTIVE == self.state

    @property
    def cancelled(self) -> bool:
        return State.CANCELED == self.state

    @property
    def ended(self) -> bool:
        return State.ENDED == self.state


def event(
    at: int | float | Callable,
    precursor: Event | List[Event] | None = None,
    priority: int | float | Callable = 0,
    label: str | None = None,
    **kwargs,
):
    def _event(func: Callable):
        return Event(
            at=at,
            precursor=precursor,
            action=func,
            priority=priority,
            label=label,
            **kwargs,
        )

    return _event
