# Continous event

The following codes shows a continous event between 1s and 1.5s. This event will act every time step during the simulation. If once set to true, then the event will only act once although it has been set to a period.

```py
from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1.5)
def hello_world():
    print(f"Hello World at {universe.time}!")

universe.set_time_resolution(1)
universe.simulate(2)
```

## Cancel a event

The continous event can be canceled at any time. Cancelled event can not be resumed because the event will be considered as ended.

```py
from Akatosh.event import Event
from Akatosh.universe import universe

hello_world = Event(1, 1.5, lambda: print("Hello World!"))
cancel = Event(1.3,1.3, lambda: hello_world.cancel())

universe.set_time_resolution(1)
universe.simulate(2)
```

## Pause a event

The continous event can be paused which allows it to resumed later. But please note the priority. If the pause event has a higher priority value, then the targeted event will still act at that time. You can still resume a event that is already passed the end time but the event will not act.

```py
from Akatosh.event import Event
from Akatosh.universe import universe

hello_world = Event(1, 1.5, lambda: print("Hello World!"), priority=1)
pause = Event(1.2,1.2, lambda: hello_world.pause()) # hello_world event will not act at 1.2 because the pause has priority 0.
resume = Event(1.4,1.4, lambda: hello_world.resume(), 1) # hellow_world event will not act at 1.4 because the pause has priority 1.

universe.set_time_resolution(1)
universe.simulate(2)
```
