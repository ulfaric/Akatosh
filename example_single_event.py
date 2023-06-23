import logging

from Akatosh import event, mundus


@event(at=5)
def hellow_world_again():
    print(f"{mundus.now}:\tHello World! Again!")
    
@event(at=1)
def hellow_world():
    print(f"{mundus.now}:\tHello World!")

mundus.set_logger(logging.DEBUG)
mundus.simulate()