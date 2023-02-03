from __future__ import annotations
from typing import Generator, List, Optional, Union, Callable, TYPE_CHECKING
from uuid import uuid4
from math import inf
import warnings

from Akatosh import Timeline, Mundus

if TYPE_CHECKING:
    from Akatosh import Resource
    from Akatosh import Producer


class Actor:

    _id: int
    _action: Optional[Generator | Callable]
    _timeline: Timeline
    _priority: int
    _at: Union[int, float]
    _step: Union[int, float, Callable]
    _till: Union[int, float]
    _active: bool
    _after: Actor

    _time: Union[int, float]
    _status: List[str]
    _followers: List[Actor]

    def __init__(
        self,
        action: Optional[Generator | Callable] = None,
        timeline: Optional[Timeline] = None,
        priority: int = 0,
        at: Union[int, float, Callable] = 0,
        step: Optional[int | float | Callable] = None,
        till: Optional[int | float | Callable] = None,
        active: bool = True,
        after: Optional[Actor] = None,
    ) -> None:

        # generate a unique id for this actor
        self._id = uuid4().int

        # assign the action to this actor
        self._action = action

        # assign the timeline to this actor
        if timeline is None:
            self._timeline = Mundus.timeline
        else:
            self._timeline = timeline
        self.timeline.actors.append(self)

        # assign the priority to this actor
        self._priority = priority

        # initialize the follower list
        self._followers = list()

        # assign the waiting target to this actor
        if after is not None:
            self._after = after
            after.followers.append(self)
            if after.priority > self.priority:
                warnings.warn(
                    message=f"Actor {self.id} has a lower priority than its waiting target {after.id}."
                )

        # initialize the time
        if callable(at):
            self._time = round(at(), 3)
        else:
            self._time = round(at, 3)

        if callable(step):
            self._step = step
        elif step is None:
            self._step = step
        else:
            self._step = round(step, 3)

        if callable(till):
            self._till = till
        elif till is not None:
            self._till = round(till, 3)
        else:
            self._till = till

        # initialize the status
        self._status = list()
        if active and after is None:
            self.status.append("active")
        else:
            self.status.append("inactive")
        if after is not None:
            self.status.append("onhold")

        # schedule the actor onto timeline
        if self.onhold is False and self.active is True:
            self.timeline.schedule(self)

    def perform(self):
        # non-continuous actor
        if self.active and self.onhold is False:
            if self.step is None and self.till is None:
                self.action()
                self.status.append("completed")
            # continuous actor but misses step size
            elif self.step is None and self.till is not None:
                raise AttributeError(f"Actor {self.id} has no step size defined.")
            # continuous actor with step size but no end time
            elif self.step is not None and self.till is None:
                self._till = inf
                while self.time < self.till:
                    self.action()
                    if callable(self.step):
                        self._time += round(self.step(), 3)
                    else:
                        self._time += round(self.step, 3)
                    yield self.timeline.schedule(self)
                self.action()
            # continuous actor with step size and end time
            elif self.step is not None and self.till is not None:
                if callable(self.till):
                    self._till = round(self.till(), 3)
                while self.time < self.till:
                    self.action()
                    if callable(self.step):
                        self._time += round(self.step(), 3)
                    else:
                        self._time += round(self.step, 3)
                    yield self.timeline.schedule(self)
                self.action()
                self.status.append("completed")

    def deactivate(self):
        if self.inactive:
            return
        else:
            self.status.remove("active")
            self.status.append("inactive")
            if self.time == self.till:
                self.status.append("completed")
            else:
                self.status.append("onhold")        
            for actor in self.followers:
                if actor.onhold:
                    actor.status.remove('onhold')
                    actor.status.remove('inactive')
                    actor.status.append('active')
                    actor._time = self.time
                    self.timeline.schedule(actor)

    def activate(self, force: bool = True):
        if self.active:
            return
        else:
            if force:
                self.status.remove("inactive")
                if self.onhold:
                    self.status.remove("onhold")
                self.status.append("active")
                self._time = self.timeline.now
                self.timeline.schedule(self)
            else:
                if self.after.completed:
                    self.status.remove("inactive")
                    if self.onhold:
                        self.status.remove("onhold")
                    self.status.append("active")
                    self._time = self.timeline.now
                    self.timeline.schedule(self)

    def request(self, resource: Resource, amount: Union[int, float] = 1) -> bool:
        resource.distribute(self, amount)

    def release(self, resource: Resource, amount: Optional[int | float] = None) -> bool:
        if amount is None:
            resource.release(self)
        else:
            resource.release(self, amount)

    def consume(self, producer: Producer, amount: Optional[int | float] = None) -> bool:
        producer.distribute(self, amount)

    @property
    def id(self):
        return self._id

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
    def time(self):
        return self._time

    @property
    def till(self):
        return self._till

    @property
    def step(self):
        return self._step

    @property
    def status(self):
        return self._status

    @property
    def after(self):
        return self._after

    @property
    def active(self):
        return "active" in self.status

    @property
    def inactive(self):
        return "inactive" in self.status

    @property
    def onhold(self):
        return "onhold" in self.status

    @property
    def scheduled(self):
        return "scheduled" in self.status

    @property
    def completed(self):
        return "completed" in self.status

    @property
    def followers(self):
        return self._followers
