import logging
from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1.5)
def hello_world():
    print(f"Hello World at {universe.time}!")
    
@event(1,1.5)
def hello_world2():
    print(f"Hello World at {universe.time}!")


universe.enable_realtime()
universe.simulate(2)