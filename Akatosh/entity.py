from abc import abstractmethod
from collections.abc import Iterable
from typing import Callable, List, Iterable
from uuid import uuid4

from Akatosh.universe import Mundus

from .event import Event, InstantEvent, ContinuousEvent
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
        self._registered_lists: List[EntityList] = list()
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
            self.unregister_from_lists()
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
            
    def unregister_from_lists(self):
        """Remove this entity from all registered entity lists."""
        for list in self.registered_lists[:]:
            list.remove(self)
            
    def continuous_event(
        self,
        at: int | float | Callable,
        interval: int | float | Callable,
        duration: int | float | Callable,
        precursor: Event | List[Event] | None = None,
        priority: int | float | Callable = 0,
        label: str | None = None,
        **kwargs,
    ):
        """A decorator for creating continous event.

        Args:
            at (int | float | Callable): when the continuous event starts.
            interval (int | float | Callable): how frequent the event happens.
            duration (int | float | Callable): the duration of the event.
            precursor (Event | List[Event] | None, optional): the precursors for this event. Defaults to None.
            priority (int | float | Callable, optional): the priority for this event. Defaults to 0.
            label (str | None, optional): short description of the event. Defaults to None.
        """

        def _continous_event(func: Callable):
            return ContinuousEvent(
                at=at,
                interval=interval,
                duration=duration,
                precursor=precursor,
                action=func,
                priority=priority,
                label=label,
                **kwargs,
            )
        
        if self.terminated:
            raise RuntimeError(f"Entity {self.label} is already terminated.")

        return _continous_event

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
    
    @property
    def registered_lists(self):
        """Return the entity lists contains the entity."""
        return self._registered_lists


class EntityList(list):
    """Customized list for entities."""
    
    def __init__(self, iterable:Iterable[Entity]):
        """Create a list for entities.

        Args:
            iterable (Iterable[Entity]): Iterable of entities.
        """
        super().__init__(item for item in iterable if isinstance(item, Entity))
        
    def insert(self, __index: int, __object: Entity) -> None:
        """Insert an entity to the list.

        Args:
            __index (SupportsIndex): the index to insert the entity.
            __object (Entity): the entity to be inserted.
        """
        super().insert(__index, __object)
        __object.registered_lists.append(self)
        
    def append(self, __object: Entity) -> None:
        """Append an entity to the list.

        Args:
            __object (Entity): the entity to be appended.
        """
        super().append(__object)
        __object.registered_lists.append(self)
        
    def remove(self, __object: Entity) -> None:
        """Remove an entity from the list.

        Args:
            __object (Entity): the entity to be removed.
        """
        super().remove(__object)
        __object.registered_lists.remove(self)
        
    def pop(self, __index: int = ...) -> Entity:
        """Pop an entity from the list.

        Args:
            __index (int, optional): the index. Defaults to ... (the last one).

        Returns:
            Entity: return the poped entity.
        """
        __object:Entity = super().pop(__index)
        __object.registered_lists.remove(self)
        return __object
    
    def clear(self) -> None:
        """Clear the list.
        """
        for item in self:
            item.registered_lists.remove(self)
        super().clear()
        
    def extend(self, __iterable: Iterable[Entity]) -> None:
        """Extend the list with an iterable of entities.

        Args:
            __iterable (Iterable[Entity]): the iterable of entities.
        """
        super().extend(__iterable)
        for item in __iterable:
            item.registered_lists.append(self)