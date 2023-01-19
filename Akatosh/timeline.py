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

    # def schedule(self, actor: Actor):
    #     self.events.append(actor)
    #     self.events.sort(key=lambda event: event.priority)
    #     self.events.sort(key=lambda event: event.scheduled_time)
    #     actor._status = 'scheduled'

    # def forward(self, till: Union[int, float]):
    #     while True:
    #         if len(self.events) != 0:
    #             next_event = self.events.pop(0)
    #             if self.now < next_event.scheduled_time:
    #                 self._time = next_event.scheduled_time
    #             if next_event.scheduled_time < till:
    #                 if inspect.isgeneratorfunction(next_event.action):
    #                     try:
    #                         next(next_event.action())
    #                     except StopIteration:
    #                         next_event._status = 'finished'
    #                 elif next_event.action is not None:
    #                     try:
    #                         next_event.action()
    #                     except Exception as e:
    #                         print(e)
    #             else:
    #                 break
    #         else:
    #             break

    def schedule(self, actor: Actor):
        event = Event(at=actor.scheduled_time, priority=actor.priority, actor=actor)
        self.events.append(event)
        self.events.sort(key=lambda event: event.priority)
        self.events.sort(key=lambda event: event.at)
        actor._status = 'scheduled'

    def forward(self, till: Union[int, float]):
        while True:
            if len(self.events) != 0:
                next_event = self.events.pop(0)
                if self.now < next_event.at:
                    self._time = next_event.at
                if next_event.at < till:
                    if inspect.isgeneratorfunction(next_event.actor.action):
                        try:
                            next(next_event.actor.action())
                        except StopIteration:
                            next_event.actor._status = 'finished'
                    elif next_event.actor.action is not None:
                        try:
                            next_event.actor.action()
                        except Exception as e:
                            print(e)
                else:
                    break
            else:
                break

    @property
    def now(self):
        return self._time

    @property
    def actors(self):
        return self._actors

    @property
    def events(self):
        return self._events
