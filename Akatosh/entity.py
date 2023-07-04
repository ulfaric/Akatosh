import re
from uuid import uuid4
from typing import Callable, List
from .event import InstantEvent
from .states import State
from .resource import Resource


class Enity:
    def __init__(self, label: str | None = None) -> None:
        self._id = uuid4().int
        self._label = label
        self._state = str()
        self._occupied_resources:List[Resource] = list()

    def create(self, at: int | float, action: Callable) -> None:
        def _create():
            self._state = State.CREATED
            self.on_creation()

        InstantEvent(at=at, action=_create, entity=self)

    def on_creation(self):
        pass

    def terminate(self, at: int | float, action: Callable) -> None:
        def _terminate():
            self._state = State.TERMINATED
            for res in self.ocupied_resources:
                res.collect(self)
            self.on_termination()

        InstantEvent(at=at, action=_terminate, entity=self)

    def on_termination(self):
        pass

    def get(self, resource: Resource, amount: int | float | Callable | None = None) -> None:
        if amount:
            if callable(amount):
                resource.distribute(self, amount())
                self.ocupied_resources.append(resource)
            else:
                resource.distribute(self, amount)
                self.ocupied_resources.append(resource)
        else:
            resource.distribute(self, resource.amount)
            
    def put(self, resource: Resource, amount: int | float | Callable | None = None) -> None:
        if amount:
            if callable(amount):
                resource.collect(self, amount())
                if self not in resource.users:
                    self.ocupied_resources.remove(resource)
            else:
                resource.put(amount)
                if self not in resource.users:
                    self.ocupied_resources.remove(resource)
        else:
            resource.put(resource.amount)
        
    @property
    def label(self):
        return self._label

    @property
    def state(self):
        return self._state

    @property
    def ocupied_resources(self):
        return self._occupied_resources