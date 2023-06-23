from __future__ import annotations

from typing import Callable, List, Tuple

from .logger import logger
from .universe import mundus


class Resource:
    def __init__(
        self,
        capacity: int | float | Callable,
        initial_amount: int | float | Callable | None = None,
        label: str | None = None,
    ) -> None:
        if callable(capacity):
            self._capacity = capacity()
        else:
            self._capacity = capacity
        if initial_amount:
            if callable(initial_amount):
                if initial_amount() > self.capacity:
                    raise ValueError("Initial amount is greater than capacity.")
                else:
                    self._amount = initial_amount()
            else:
                if initial_amount > self.capacity:
                    raise ValueError("Initial amount is greater than capacity.")
                else:
                    self._amount = initial_amount
        else:
            self._amount = self.capacity
        self._label = label
        self._records: List[Tuple[object, int | float]] = list()
        self._usage_records: List[Tuple[int | float, int | float]] = list()

    def get(self, amount: int | float) -> None:
        if amount > self.amount:
            raise ValueError(f"Not enough amount in Resource {self.label}.")
        else:
            self._amount -= amount
            self.usage_records.append((mundus.now, self.amount))

    def put(self, amount: int | float) -> None:
        if amount > self.occupied:
            raise ValueError(f"Not enough capacity in Resource {self.label}.")
        else:
            self._amount += amount
            self.usage_records.append((mundus.now, self.amount))

    def distribute(self, user: object, amount: int | float) -> None:
        if amount > self.amount:
            raise ValueError(f"Not enough amount in Resource {self.label}.")
        else:
            self._amount -= amount
            if user in self.users:
                for index, record in enumerate(self.records):
                    if record[0] is user:
                        self.records[index] = (user, record[1] + amount)
                        break
            else:
                self.records.append((user, amount))
            self.usage_records.append((mundus.now, self.amount))
            logger.debug(f"Resource {self.label} distributed {amount} to {user}.")

    def collect(self, user: object, amount: int | float | None = None) -> None:
        if user not in self.users:
            raise ValueError(f"User {user} is not using Resource {self.label}.")
        if amount is None:
            for index, record in enumerate(self.records):
                if record[0] is user:
                    self._amount += record[1]
                    self.usage_records.append((mundus.now, self.amount))
                    logger.debug(
                        f"Resource {self.label} collected {amount} from {user}."
                    )
                    break
        else:
            for index, record in enumerate(self.records):
                if record[0] is user:
                    if record[1] < amount:
                        raise ValueError(
                            f"{user} occupied {record[1]} of Resource {self.label}, less than {amount}."
                        )
                    else:
                        self.records[index] = (user, record[1] - amount)
                        self._amount += amount
                        self.usage_records.append((mundus.now, self.amount))
                        logger.debug(
                            f"Resource {self.label} collected {amount} from {user}."
                        )
                        break

    def usage(self, duration: int | float | Callable | None = None):
        if duration:
            if callable(duration):
                after = mundus.now - duration()
            else:
                after = mundus.now - duration
            if after < 0:
                after = 0
            usage_records = [
                usage_record
                for usage_record in self.usage_records
                if usage_record[0] >= after
            ]
            if len(usage_records) == 0:
                return 1 - (self.amount / self.capacity)
            else:
                if usage_records[-1][0] - after == 0:
                    return 1 - (usage_records[-1][1] / self.capacity)
                else:
                    weighted_overall_amount = 0
                    for index, record in enumerate(usage_records):
                        if index == 0:
                            weighted_overall_amount += record[1] * (record[0] - after)
                        elif index == len(usage_records) - 1:
                            weighted_overall_amount += record[1] * (
                                mundus.now - usage_records[index - 1][0]
                            )
                        else:
                            weighted_overall_amount += record[1] * (
                                record[0] - usage_records[index - 1][0]
                            )
                    return 1 - (
                        weighted_overall_amount / (usage_records[-1][0] - after)
                    )
        else:
            return 1 - (self.amount / self.capacity)

    @property
    def amount(self) -> int | float:
        return self._amount

    @property
    def capacity(self) -> int | float:
        return self._capacity

    @property
    def occupied(self) -> int | float:
        return self.capacity - self.amount

    @property
    def label(self) -> str | None:
        return self._label

    @property
    def records(self) -> List[Tuple[object, int | float]]:
        return self._records

    @property
    def usage_records(self) -> List[Tuple[int | float, int | float]]:
        return self._usage_records

    @property
    def users(self) -> List[object]:
        return [record[0] for record in self._records]
