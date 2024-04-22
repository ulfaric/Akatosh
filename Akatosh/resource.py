from math import inf
from typing import List, Tuple

from . import logger
from .entity import Entity


class Resource:

    def __init__(self, capacity: float, usage: float = 0.0) -> None:
        self._capacity = capacity
        self._usage = usage
        self._users: List[Tuple[Entity, float]] = list()

    def distribute(self, user: Entity, amount: float = inf) -> bool:
        """Distribute the given amount of resource to the user."""
        if amount == inf:
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._users[index] = (user, self.users[index][1] + self.level)
                self._usage += self.level
            else:
                self._usage += self.level
                self.users.append((user, self.level))
                user.occupied_resources.append(self)
            logger.debug(f"{self} distributed all available resource to {user}.")
            return True

        if self.level > amount:
            self._usage += amount
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._users[index] = (user, self.users[index][1] + amount)
            else:
                self.users.append((user, amount))
                user.occupied_resources.append(self)
            logger.debug(f"{self} distributed {amount} to {user}.")
            return True
        else:
            logger.warn(f"{self} cannot distribute {amount} to {user}. Not enough resource.")
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._users[index] = (user, self.users[index][1] + self.level)
                self._usage += self.level
            else:
                self._usage += self.level
                self.users.append((user, self.level))
                user.occupied_resources.append(self)
            logger.debug(f"{self} distributed all available resource to {user}.")
            return False

    def collect(self, user: Entity, amount: float = inf) -> bool:
        """Collect the resource from the user. If the amount is infinite, the user will be removed from the users list and all amount will be collected."""
        if amount == inf:
            existing_users = [user[0] for user in self.users]
            if user in existing_users:
                index = existing_users.index(user)
                self._usage -= self.users[index][1]
                self.users.pop(index)
                user.occupied_resources.remove(self)
                logger.debug(f"{self} collected all occupied resource from {user}.")
                return True
            else:
                logger.warn(f"{self} cannot collect resource from non-user {user}.")
                return False

        existing_users = [user[0] for user in self.users]
        if user in existing_users:
            index = existing_users.index(user)
            if self.users[index][1] > amount:
                self._usage -= amount
                self._users[index] = (user, self.users[index][1] - amount)
                return True
            else:
                logger.warn(f"{self} cannot collect {amount} from {user}. Not enough resource occupied by the user.")
                self._usage -= self.users[index][1]
                self.users.pop(index)
                user.occupied_resources.remove(self)
                logger.debug(f"{self} collected all occupied resource from {user}.")
                return False
        else:
            logger.warn(f"{self} cannot collect resource from non-user {user}.")
            return False

    def reset(self) -> None:
        """Reset the resource level and users."""
        self._usage = 0.0
        for user in self.users:
            user[0].occupied_resources.remove(self)
        self._users.clear()

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def usage(self) -> float:
        return self._usage

    @property
    def level(self) -> float:
        return self.capacity - self.usage

    @property
    def users(self) -> List[Tuple[Entity, float]]:
        return self._users
