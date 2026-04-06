from env import RescueEnv
from agent import choose_action

env = RescueEnv()
state = env.reset()

print("Initial State:", state)

for step in range(20):
    action = choose_action(state)

    state, reward, done = env.step(action)

    print(f"Step {step+1}")
    print("Action:", action)
    print("State:", state)
    print("Reward:", reward)
    print("Done:", done)
    print("-" * 30)

    if done:
        print("✅ Reached victim!")
        break