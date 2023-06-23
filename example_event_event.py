import logging

from Akatosh import event, mundus
    
@event(at=1)
def hellow_world():
    print(f"{mundus.now}:\tHello World!")
    
    @event(at=5)
    def hellow_world_again():
        print(f"{mundus.now}:\tHello World! Again!")

mundus.set_logger(logging.DEBUG)
mundus.simulate()