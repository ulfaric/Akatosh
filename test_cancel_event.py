from Akatosh.event import Event
from Akatosh.universe import universe

hello_world = Event(1, 1.5, lambda: print("Hello World!"))
cancel = Event(1.3,1.3, lambda: hello_world.cancel())

universe.set_time_resolution(1)
universe.simulate(2)