from Akatosh.event import Event
from Akatosh.universe import Mundus

event1 = Event(at=2, action=lambda: print("Genesis!"), label="Genesis")

event2 = Event(at=0, after=[event1], action=lambda: print("Hello, World!"), label="Hello World")

Mundus.simulate()