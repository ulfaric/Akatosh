# Real Time Simulation

This is a unique feature of Akatosh that it is capable of simulting event in real time. It is achieved by carefully using the combination of while loop and asyncio.sleep which gurantees the simulation time step is sync with real time. In each time step, the event will be executed based on their priorities. As long as the execution time of your scheduled event is not exceeding the time step resolution (defualt to 1ms), your events will be in sync with real time.

If your time step is set to very small (less than a couple of ms), you may cause time out error and the event will not be executed futher. This is to follow a IEC 61131 - 3 style.

```py
import asyncio
from Akatosh.event import event
from Akatosh.universe import Mundus


@event(1, 1.5)
def hello_world():
    print(f"Hello World at {Mundus.time}!")

Mundus.enable_realtime(2)
asyncio.run(Mundus.simulate(2))
```

The above codes will print "Hello World at {Mundus.time}" every 10ms fromm 1s to 1.5s!

## Time Scale

You can also set time scale to make the real time simulation run faster than realtime. (Please note that relativity theory will not be considered if your time scale is huge...)

```py
Mundus.set_timescale(5) # this will make simulation run 5x faster than real time!
```

You can change the time scale at any time while the simulation is runing, even with a event itself.

## Pause and Resume

You can also pause and resume the simulation.

```py
Mundus.pause() # this will pause the simulation.
Mundus.resume() # this will resume the simulation.
```

Technically, this should works for non-real time mode too.

## Watchdog

Unlike the standard in IEC 61131 - 3, if a event/task exceeded the deadline, the whole program will stop. In Akatosh, only the event/task itself will stop if it is a cotinouse event. But additionally, you can define a watchdog function as pass it when create a event. Then, the wacthdog event will be execued when exceeding deadline happens.

```py
def watchdog():
    print(f"Watchdog bite!")
hello_world = Event(0,5,lambda: print(f"Hello world at {Mundus.time}"), 0.0005, watchdog=watchdog)
```

The above example will trigger watchdog function if hello world is not printed in time of 0.5 ms.
