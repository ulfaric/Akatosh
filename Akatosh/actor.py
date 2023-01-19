import inspect
from typing import Generator, List, Optional, Union, Callable
from uuid import uuid4

from Akatosh import Event, Timeline, UNIVERSE


class Actor:

    _id: int
    _action: Optional[Generator | Callable]
    _timeline: Timeline
    _priority: int
    _at: Union[int, float]

    _scheduled_time: Union[int, float]
    _status: str

    def __init__(
        self,
        action: Optional[Generator | Callable] = None,
        timeline: Optional[Timeline] = None,
        priority: int = 0,
        at: Union[int, float] = 0,
    ) -> None:
        # generate a unique id for this actor
        self._id = uuid4().int
        # assign the action to this actor
        self._action = action
        # assign the timeline to this actor
        if timeline is None:
            self._timeline = UNIVERSE.primary_timeline
        else:
            self._timeline = timeline
        self.timeline.actors.append(self)
        # assign the priority to this actor
        self._priority = priority

        # initialize the time
        self._scheduled_time = at

        # initialize the status
        self._status = str()

        # schedule the actor onto timeline
        self.timeline.schedule(self)

    def wait(self, till: Union[int, float]) -> None:
        self._scheduled_time += till
        self.timeline.schedule(self)

    @property
    def priority(self):
        return self._priority

    @property
    def action(self):
        return self._action

    @property
    def timeline(self):
        return self._timeline

    @property
    def scheduled_time(self):
        return self._scheduled_time