from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, List
from uuid import uuid4

from .logger import logger
from .states import State
from .universe import mundus


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
        self._id = uuid4().int
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

    @abstractmethod
    async def _perform(self):
        pass

    def __eq__(self, _o: Event) -> bool:
        return self.id == _o.id

    @property
    def id(self) -> int:
        return self._id

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


class InstantEvent(Event):

    async def _perform(self):
        if self.action:
            self.action()
        # mundus.current_events.remove(self)
        # mundus.past_events.append(self)
        self._end()
        logger.debug(f"Event {self.label} is ended.")


def event(
    at: int | float | Callable,
    precursor: Event | List[Event] | None = None,
    priority: int | float | Callable = 0,
    label: str | None = None,
    **kwargs,
):
    def _event(func: Callable):
        return InstantEvent(
            at=at,
            precursor=precursor,
            action=func,
            priority=priority,
            label=label,
            **kwargs,
        )

    return _event


class ContinousEvent(Event):
    def __init__(
        self,
        at: int | float | Callable[..., Any],
        step: int | float | Callable[..., Any],
        duration: int | float | Callable[..., Any],
        precursor: Event | List[Event] | None = None,
        action: Callable[..., Any] | None = None,
        priority: int | float | Callable[..., Any] = 0,
        label: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            at=at,
            precursor=precursor,
            action=action,
            priority=priority,
            label=label,
            **kwargs,
        )
        self._step = step
        if callable(duration):
            self._duration = round(duration(), mundus.resolution)
        else:
            self._duration = round(duration, mundus.resolution)
        self._sub_events: List[InstantEvent] = list()

    async def _perform(self):
        if self.action:
            if mundus.now <= self.at + self.duration:
                self.action()
                if callable(self.step):
                    next_step = round(self.step(), mundus.resolution) + mundus.now
                else:
                    next_step = round(self.step, mundus.resolution) + mundus.now
                if next_step <= self.at + self.duration:
                    self.sub_events.append(
                        InstantEvent(
                            at=next_step,
                            step=self.step,
                            duration=self.duration,
                            precursor=self.precursor,
                            action=self._perform,
                            priority=self.priority,
                            label=self.label,
                        )
                    )
                    logger.debug(f"Event {self.label} next step is at {next_step}.")
                else:
                    logger.debug(f"Event {self.label} is ended.")

    @property
    def step(self) -> int | float | Callable[..., Any]:
        return self._step

    @property
    def duration(self) -> int | float:
        return self._duration

    @property
    def sub_events(self) -> List[InstantEvent]:
        return self._sub_events
