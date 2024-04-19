from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING, Callable, List, Optional

from . import logger
from .event import Event
from .universe import universe

if TYPE_CHECKING:
    from .resource import Resource


class Entity:

    def __init__(self, at: float | Event, till: float | Event, label: Optional[str] = None, priority:int = 1) -> None:
        self._label = label
        self._at = at
        self._till = till
        self._created = False
        self._terminated = False
        self._priority = priority

        # create an instant creation event
        self._creation = Event(at, inf, self._create, f"{self} Creation", once=True)
        self._termination = Event(till, inf, self._terminate, f"{self} Termination", once=True)

        # create a queue for engaged events
        self._events: List[Event] = list()

        # create a queue for acquired resources
        self._occupied_resources: List[Resource] = list()

    def __str__(self) -> str:
        if self.label is None:
            return f"Entity\t{id(self)}"
        return self.label

    def _create(self):
        self._created = True
        logger.debug(f"Entity\t{self}\tcreated.")

    def _terminate(self):
        self._terminated = True
        for event in self.events:
            event.cancel()
        for resource in self.occupied_resources:
            resource.collect(self, inf)
        logger.debug(f"Entity\t{self}\tterminated.")

    def event(self, at: float | Event, till: float | Event, label: Optional[str] = None, once: bool = False, priority: int = 1):

        def _event(action: Callable):

            async def __event():
                
                if self.terminated:
                    logger.warn(f"Entity\t{self}\talready terminated.")
                    return

                while True:
                    if not self.created:
                        logger.warn(f"Entity\t{self}\tnot created yet.")
                        await universe.time_flow
                    else:
                        break

                event = Event(at, till, action, label, once, priority)
                self.events.append(event)
                logger.debug(f"Event\t{event}\tadded to entity\t{self}.")

            Event(at, at, __event, f"{label}\tEngagement", True)

        return _event

    def acquire(self, resource: Resource, amount: float) -> bool:
        if resource.distribute(self, amount):
            self.occupied_resources.append(resource)
            logger.debug(f"Entity\t{self}\tacquired\t{amount}\tof resource\t{resource}.")
            return True
        else:
            return False

    def release(self, resource: Resource, amount: float) -> bool:
        if resource.collect(self, amount):
            self.occupied_resources.remove(resource)
            logger.debug(f"Entity\t{self}\treleased\t{amount}\tof resource\t{resource}.")
            return True
        else:
            return False

    @property
    def label(self):
        return self._label

    @property
    def created(self):
        return self._created

    @property
    def terminated(self):
        return self._terminated

    @property
    def events(self):
        return self._events

    @property
    def occupied_resources(self):
        return self._occupied_resources

    @property
    def priority(self):
        return self._priority