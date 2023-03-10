from Akatosh import Actor, Mundus

Mundus.accuracy = 4

test_actor = Actor(at=0, step=0.00004, till=0.06, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is running."))
test_actor2 = Actor(at=0, step=0.00004, till=0.07, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 2 is running."))

# def deactive_test_actor1():
#     test_actor.deactivate()
#     print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is deactived.")

# test_actor3= Actor(at=3, action=deactive_test_actor1)
# test_actor4 = Actor(after=[test_actor, test_actor2],step=0.001, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor2.priority}:\tTest Actor 4 is running."))

Mundus.simulate(1.5)