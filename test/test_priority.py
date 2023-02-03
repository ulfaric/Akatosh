from Akatosh import Actor, Mundus

test_actor = Actor(at=0, step=0.001, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor is running."))
test_actor2 = Actor(at=2,step=0.001, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor2.priority}:\tTest Actor 2 is running."))
test_actor3 = Actor(at=3,step=0.001, priority=1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor3.priority}:\tTest Actor 3 is running."))

Mundus.simulate(5)