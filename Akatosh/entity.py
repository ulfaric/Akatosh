from abc import abstractmethod
from typing import Callable, List
from uuid import uuid4

from Akatosh.universe import Mundus

from .event import InstantEvent
from .resource import Resource
from .states import State
from .logger import logger


class Entity:
    def __init__(
        self,
        label: str | None = None,
        create_at: int | float | Callable | None = None,
        terminate_at: int | float | Callable | None = None,
    ) -> None:
        self._id = uuid4().int
        self._label = label
        self._state: List[str] = list()
        self._occupied_resources: List[Resource] = list()
        self._creation: InstantEvent = None  # type: ignore
        self._termination: InstantEvent = None  # type: ignore

        if create_at is not None:
            if callable(create_at):
                self.create(at=round(create_at(), Mundus.resolution))
            else:
                self.create(at=round(create_at, Mundus.resolution))

        if terminate_at is not None:
            if callable(terminate_at):
                self.terminate(at=round(terminate_at(), Mundus.resolution))
            else:
                self.terminate(at=round(terminate_at, Mundus.resolution))

    def create(self, at: int | float) -> None:
        def _create():
            if self.terminated:
                raise RuntimeError(f"Entity {self.label} is already terminated.")
            self._state.append(State.CREATED)
            self.on_creation()
            logger.debug(f"Entity {self.label} created at {Mundus.now}")

        self._creation = InstantEvent(
            at=at, action=_create, label=f"Creation of {self.label}"
        )

    @abstractmethod
    def on_creation(self):
        pass

    def terminate(self, at: int | float) -> None:
        def _terminate():
            if not self.created:
                raise RuntimeError(f"Entity {self.label} is not created yet.")
            self._state.append(State.TERMINATED)
            self.release_resources()
            self.on_termination()
            logger.debug(f"Entity {self.label} terminated at {Mundus.now}")

        self._termination = InstantEvent(
            at=at, action=_terminate, label=f"Termination of {self.label}"
        )

    @abstractmethod
    def on_termination(self):
        pass

    def get(
        self, resource: Resource, amount: int | float | Callable | None = None
    ) -> None:
        if amount:
            if callable(amount):
                resource.distribute(self, amount())
                self.ocupied_resources.append(resource)
            else:
                resource.distribute(self, amount)
                self.ocupied_resources.append(resource)
        else:
            resource.distribute(self, resource.amount)

    def put(
        self, resource: Resource, amount: int | float | Callable | None = None
    ) -> None:
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

    def release_resources(self):
        for res in self.ocupied_resources:
            res.collect(self)

    @property
    def label(self):
        return self._label

    @property
    def state(self):
        return self._state

    @property
    def created(self):
        return State.CREATED in self.state

    @property
    def terminated(self):
        return State.TERMINATED in self.state

    @property
    def ocupied_resources(self):
        return self._occupied_resources
