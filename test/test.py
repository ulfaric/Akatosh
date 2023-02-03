from Akatosh import Mundus, Actor

class mom(Actor):

    def __init__(self, at, step, priority, name) -> None:
        super().__init__(at=at, step=step, priority=priority)
        self._name = name
        self._num_children = 0

    def action(self):
        c = child(at=self.timeline.now, step=1, till=10, priority=-self._num_children, name=f"Child-{self._num_children}")
        self._num_children += 1
        print(f"Time: {Mundus.now}\tEvent Priority: {self.priority}:\t{self._name} picks up a child {c._name}.")

        if self.timeline.now >= 3:
            self.deactivate()

class child(Actor):

    def __init__(self, at, step, till, priority, name) -> None:
        super().__init__(at=at, step=step, till=till, priority=priority)
        self._name = name

    def action(self):
        print(f"Time: {Mundus.now}\tEvent Priority: {self.priority}:\t{self._name}\tis playing at home.")
        if self.timeline.now >= 5 and self.timeline.now<7:
            uncle.deactivate()
        if self.timeline.now >= 7:
            uncle.activate(force=False)

m = mom(at=0, step=1, priority=0, name="Mom")
father = Actor(after=m, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {father.priority}:\tFather comes back home."))
grandpa = Actor(after=m, step=1, till=10, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {grandpa.priority}:\tGrandpa comes back home."))
uncle = Actor(after=[father, grandpa], step=1, till=10, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {uncle.priority}:\tUncle comes to vist."))

Mundus.simulate(10)
print(m.status)
print(father.status)
print(uncle.status)
