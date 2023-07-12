import logging

from Akatosh import instant_event, Mundus


@instant_event(at=1)
def hellow_world():
    print(f"{Mundus.now}:\tHello World!")

    @instant_event(at=5)
    def hellow_world_again():
        print(f"{Mundus.now}:\tHello World! Again!")


Mundus.set_logger(logging.DEBUG)
Mundus.simulate()
