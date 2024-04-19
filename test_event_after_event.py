from Akatosh.event import Event
from Akatosh.universe import universe

hello = Event(0.5, 0.5, lambda: print("Hello"))
world = Event(hello, 0.5, lambda: print("World"))

universe.set_time_resolution(1)
universe.simulate(1)