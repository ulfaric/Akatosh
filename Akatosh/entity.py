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
        """Create a entity.

        Args:
            label (str | None, optional): short description of the entity. Defaults to None.
            create_at (int | float | Callable | None, optional): when the life cycle of this entity should start. Defaults to None, then must call create() method manually.
            terminate_at (int | float | Callable | None, optional): when the life cycle of this entity should end. Defaults to None, then must call terminate() method manually.
        """
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
        """The creation of the entity."""
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
        """Callback function upon creation of the entity"""
        pass

    def terminate(self, at: int | float) -> None:
        """The termination of the entity."""
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
        """Callback function upon termination of the entity"""
        pass

    def get(
        self, resource: Resource, amount: int | float | Callable | None = None
    ) -> None:
        """Consume certain amout from a resource. if no amount is specified, consume all."""
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
        """Return certain amout to a resource. if no amount is specified, return all."""
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
        """Release all occupied resources."""
        for res in self.ocupied_resources:
            res.collect(self)

    @property
    def label(self):
        """Return the label of the entity."""
        return self._label

    @property
    def state(self):
        """Return the state(s) of the entity."""
        return self._state

    @property
    def created(self):
        """Return True if the entity is created."""
        return State.CREATED in self.state

    @property
    def terminated(self):
        """Return True if the entity is terminated."""
        return State.TERMINATED in self.state

    @property
    def ocupied_resources(self):
        """Return the resources occupied by the entity."""
        return self._occupied_resources
