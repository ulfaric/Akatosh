import logging

from Akatosh import event, Mundus


@event(at=1)
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

    @event(at=5)
    def hellow_world_again():
        print(f"{Mundus.now}:\tHello World! Again!")


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
