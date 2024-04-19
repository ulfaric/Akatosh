from math import inf
from typing import List, Tuple

from .entity import Entity


class Resource:

    def __init__(self, capacity: float, level: float = 0.0) -> None:
        self._capacity = capacity
        self._level = level
        self._users: List[Tuple[Entity, float]] = list()

    def distribute(self, user: Entity, amount: float = inf) -> bool:
        """Distribute the given amount of resource to the user."""
        if amount == inf:
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._users[index] = (user, self.users[index][1] + self.amount)
                self._level += self.amount
                return True
            else:
                self._level += self.amount
                self.users.append((user, self.amount))
                return True

        if self.amount > amount:
            self._level += amount
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._users[index] = (user, self.users[index][1] + amount)
            else:
                self.users.append((user, amount))
            return True
        else:
            return False

    def collect(self, user: Entity, amount: float = inf) -> bool:
        """Collect the resource from the user. If the amount is infinite, the user will be removed from the users list and all amount will be collected."""
        if amount == inf:
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._level -= self.users[index][1]
                self.users.pop(index)
                return True
            else:
                return False

        existing_users = [user[0] for user in self.users]
        if user in existing_users:
            index = existing_users.index(user)
            if self.users[index][1] >= amount:
                self._level -= amount
                self._users[index] = (user, self.users[index][1] - amount)
                return True
            else:
                return False
        else:
            return False

    def reset(self) -> None:
        """Reset the resource level and users."""
        self._level = 0.0
        for user in self.users:
            user[0].occupied_resources.remove(self)
        self._users.clear()

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def level(self) -> float:
        return self._level

    @property
    def amount(self) -> float:
        return self.capacity - self.level

    @property
    def users(self) -> List[Tuple[Entity, float]]:
        return self._users
