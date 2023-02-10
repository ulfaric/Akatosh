from Akatosh import Actor, Mundus

test_actor = Actor(at=0, step=1, till=2, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is running."))
test_actor2 = Actor(at=0, step=1, till=3, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 2 is running."))
test_actor3 = Actor(after=[test_actor, test_actor2],step=1, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor2.priority}:\tTest Actor 3 is running."))

Mundus.simulate(5)