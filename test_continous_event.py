from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1.5)
def hello_world():
    print(f"Hello World at {universe.time}!")

universe.set_time_resolution(1)
universe.simulate(2)