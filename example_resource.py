import logging
from Akatosh import Resource, instant_event, Mundus

res = Resource(100, label="test")

for i in range(10):

    @instant_event(at=i, label=f"consumer{i}")
    def consumer():
        res.get(10)
        print(f"{Mundus.now} get {res.amount}, current usage {res.usage()}")


for i in range(5):

    @instant_event(at=i, label=f"producer{i}")
    def consumer():
        res.put(10)
        print(f"{Mundus.now} put {res.amount}, current usage {res.usage()}")


for i in range(10):

    @instant_event(at=i, label=f"producer{i}")
    def consumer():
        print(f"{Mundus.now} past 2s usage {res.usage(2)}")


Mundus.simulate()
