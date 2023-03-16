from __future__ import annotations

from typing import TYPE_CHECKING, List, Union
from uuid import uuid4
import inspect

from Akatosh import Event

if TYPE_CHECKING:
    from Akatosh import Actor


class Timeline:
    _id: int
    _time: Union[int, float]
    _actors: List[Actor]
    _events: List[Event]

    def __init__(self) -> None:
        self._id = uuid4().int
        self._time = 0
        self._actors = list()
        self._events = list()

    def schedule(self, actor: Actor):
        event = Event(at=actor.time, priority=actor.priority, actor=actor)
        self.events.append(event)
        self.events.sort(key=lambda event: event.priority)
        self.events.sort(key=lambda event: event.at)
        if actor.scheduled is False:
            actor.status.append('scheduled')

    def forward(self, till: Union[int, float]):
        while True:
            if len(self.events) != 0:
                next_event = self.events.pop(0)
                if self.now < next_event.at:
                    self._time = next_event.at
                if next_event.at <= till:
                    try:
                        next(next_event.actor.perform())
                    except StopIteration:
                        pass
                else:
                    break
            else:
                break
            
    def print_events(self):
        for event in self.events:
            print(f"{event.at}\t{event.priority}\t{event.actor}\t{event.actor.status}")
            
    @property
    def now(self):
        return self._time

    @property
    def actors(self):
        return self._actors

    @property
    def events(self):
        return self._events
