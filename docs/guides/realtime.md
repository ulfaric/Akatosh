# Real Time Simulation

This is a unique feature of Akatosh that it is capable of simulting event in real time. It is achieved by carefully using the combination of while loop and asyncio.sleep which gurantees the simulation time step is sync with real time. In each time step, the event will be executed based on their priorities. As long as the execution time of your scheduled event is not exceeding the time step resolution (defualt to 1ms), your events will be in sync with real time.

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