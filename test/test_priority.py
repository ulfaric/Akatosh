from Akatosh import Actor, Mundus

test_actor = Actor(at=0, step=1, till=5, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is running."))
test_actor2 = Actor(at=0, step=1, till=3, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 2 is running."))

def deactive_test_actor1():
    test_actor.deactivate()
    print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is deactived.")

test_actor3= Actor(at=3, action=deactive_test_actor1)
test_actor4 = Actor(after=[test_actor, test_actor2],step=1, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor2.priority}:\tTest Actor 4 is running."))

Mundus.simulate(5)
print(test_actor.status)
print(test_actor2.status)
print(test_actor3.status)
print(test_actor4.status)