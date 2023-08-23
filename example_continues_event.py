import random
from Akatosh import ContinuousEvent, Mundus, continuous_event, instant_event
import logging

# define a function for first continuous event
def action():
    print(f"Hello World at {Mundus.now} from Test 1")

# create a continuous event start at 0s and last 10s
event = ContinuousEvent(
    at=0, interval=random.random(), duration=10, action=action, label="Test"
)

# define a function for second continuous event
def action2():
    print(f"Hello World at {Mundus.now} from Test 2")

# create a continuous event start at 8s and last 12s but with the first event as precursor
event2 = ContinuousEvent(
    at=8,
    interval=random.random(),
    duration=12,
    action=action2,
    label="Test2",
    priority=-1,
    precursor=[event],
)

# create a instant event to terminate the first continuous event
@instant_event(at=3, label="End Test 1")
def end_event():
    event.end()

# create a third continuous event with decorator
@continuous_event(at=0, interval=random.random(), duration=15, label="Test3")
def action3():
    print(f"Hello World at {Mundus.now} from Test 3")

# enable debug message
# Mundus.set_logger(logging.DEBUG)

# run simulation
Mundus.simulate()
