import logging
from Akatosh import Resource, event, mundus

res = Resource(100,label="test")

for i in range(10):
    @event(at=i, label=f"consumer{i}")
    def consumer():
        res.get(10)
        print(f"{mundus.now} get {res.amount}, current usage {res.usage()}")
        
for i in range(5):
    @event(at=i, label=f"producer{i}")
    def consumer():
        res.put(10)
        print(f"{mundus.now} put {res.amount}, current usage {res.usage()}")
        
for i in range(10):
    @event(at=i, label=f"producer{i}")
    def consumer():
        print(f"{mundus.now} past 2s usage {res.usage(2)}")   
        
mundus.simulate()