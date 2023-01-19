from re import T
from Akatosh import UNIVERSE, Actor

class mom(Actor):

    def __init__(self, at, priority, name) -> None:
        super().__init__(at=at, priority=priority)
        self._name = name
        self._num_children = 0

    def action(self):
        while self.timeline.now<4:
            c = child(at=self.timeline.now, priority=-self._num_children, name=f"Child-{self._num_children}")
            self._num_children += 1
            print(f"Time: {self.timeline.now}:\t{self._name} delivered a child {c._name}.")
            yield self.wait(1)

class child(Actor):

    def __init__(self, at, priority, name) -> None:
        super().__init__(at=at, priority=priority)
        self._name = name

    def action(self):
        while True:
            print(f"Time: {self.timeline.now}:\t{self._name}\tis playing.")
            yield self.wait(1)

mom = mom(at=0, priority=0, name="Mom")
father = Actor(at=4, priority=0, action=lambda: print("Father is working."))

UNIVERSE.simulate(10)
