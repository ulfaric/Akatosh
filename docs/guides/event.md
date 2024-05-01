# Event

In Akatosh, "Any thing that is going to happen" is described as an event.

## Instant event

If a event has the at and till set to the same time, then the event is instant which means it only happens once at the given time.

```py
import asyncio
from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1.5,1.5) # a simple instant event which 
def hello_world():
    print(f"Hello World at {universe.time}!")

universe.set_time_resolution(1)
asyncio.run(universe.simulate(2))
```

## Continous event

The following codes shows a continous event between 1s and 1.5s. This event will act every time step during the simulation. If once set to true, then the event will only act once although it has been set to a period.

```py
import asyncio
from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1.5)
def hello_world():
    print(f"Hello World at {universe.time}!")

universe.set_time_resolution(1)
asyncio.run(universe.simulate(2))
```

## Cancel a event

The continous event can be canceled at any time. Cancelled event can not be resumed because the event will be considered as ended.

```py
import asyncio
from Akatosh.event import Event
from Akatosh.universe import universe

hello_world = Event(1, 1.5, lambda: print("Hello World!"))
cancel = Event(1.3,1.3, lambda: hello_world.cancel())

universe.set_time_resolution(1)
asyncio.run(universe.simulate(2))
```

## Pause a event

The continous event can be paused which allows it to resumed later. But please note the priority. If the pause event has a higher priority value, then the targeted event will still act at that time. You can still resume a event that is already passed the end time but the event will not act.

```py
import asyncio
from Akatosh.event import Event
from Akatosh.universe import universe

hello_world = Event(1, 1.5, lambda: print("Hello World!"), priority=1)
pause = Event(1.2,1.2, lambda: hello_world.pause()) # hello_world event will not act at 1.2 because the pause has priority 0.
resume = Event(1.4,1.4, lambda: hello_world.resume(), 1) # hellow_world event will not act at 1.4 because the pause has priority 1.

universe.set_time_resolution(1)
asyncio.run(universe.simulate(2))
```

## Make a event wait for another event

The following code print "hello world" at 0.5s by two events. The order of the word is ensured by let the world event wait for hello event.

```py
import asyncio
from Akatosh.event import Event
from Akatosh.universe import universe

hello = Event(0.5, 0.5, lambda: print("Hello"))
world = Event(hello, 0.5, lambda: print("World"))

universe.set_time_resolution(1)
asyncio.run(universe.simulate(1))
```

## Create an event within an event

The following codes demenstrate how to create a event within a event. Please note that the new event must be created after the current event.

```py
import asyncio
from Akatosh.event import event
from Akatosh.universe import universe

@event(0.5, 0.5)
def hello():
    print("Hello")
    
    @event(0.6,0.6) # new event must be after the current event
    def world():
        print("World")
    
universe.set_time_resolution(1)
asyncio.run(universe.simulate(1))
```

## Handle events at the same time

The order for events which are scheduled at the same time to happen can be determined by the priority.

```py
import asyncio
from Akatosh.event import event
from Akatosh.universe import universe

    
@event(1,1, "Event 2", once=True, priority=2)
def event2():
    print("World")
    
@event(1,1, "Event 1", once=True, priority=1)
def event1():
    print("Hello")

universe.set_time_resolution(0)
asyncio.run(universe.simulate(2))
```
