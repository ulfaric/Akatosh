```py
from Akatosh import Resource, event, Mundus

# create a resource with capacity 100
res = Resource(100, label="test")

for i in range(10):
    # get 10 units per second for 10s
    @event(at=i, label=f"consumer{i}")
    def consumer():
        res.get(10)
        print(f"{Mundus.now} get {res.amount}, current usage {res.usage()}")


for i in range(5):
    # put 10 units per second for first 5s
    @event(at=i, label=f"producer{i}")
    def consumer():
        res.put(10)
        print(f"{Mundus.now} put {res.amount}, current usage {res.usage()}")


for i in range(10):
    # report the usage every second for 10s, tracing back for 2s
    @event(at=i, label=f"producer{i}")
    def consumer():
        print(f"{Mundus.now} past 2s usage {res.usage(2)}")

# run the simulation
Mundus.simulate()
```