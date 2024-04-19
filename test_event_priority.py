from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1, "Event 2", once=True, priority=2)
def event2():
    print("World")
    
@event(1,1, "Event 1", once=True, priority=1)
def event1():
    print("Hello")

universe.set_time_resolution(0)
universe.simulate(2)