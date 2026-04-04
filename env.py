import random

class RescueEnv:
    def __init__(self, size=5):
        self.size = size
        self.reset()

    def reset(self):
        # Agent position
        self.agent_pos = [0, 0]

        # Random victim position
        self.victim_pos = [
            random.randint(0, self.size - 1),
            random.randint(0, self.size - 1)
        ]

        # State variables
        self.steps = 0
        self.max_steps = 20
        self.done = False

        return self.get_state()

    def get_state(self):
        return {
            "agent_pos": self.agent_pos,
            "victim_pos": self.victim_pos,
            "steps": self.steps
        }

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True

        # Move agent
        if action == "UP":
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == "DOWN":
            self.agent_pos[0] = min(self.size - 1, self.agent_pos[0] + 1)
        elif action == "LEFT":
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == "RIGHT":
            self.agent_pos[1] = min(self.size - 1, self.agent_pos[1] + 1)

        reward = -0.1  # step penalty

        # Check if rescued
        if self.agent_pos == self.victim_pos:
            reward = 1
            self.done = True

        self.steps += 1

        # End if max steps reached
        if self.steps >= self.max_steps:
            self.done = True

        return self.get_state(), reward, self.done



if __name__ == "__main__":
    env = RescueEnv()
    state = env.reset()

    print("Initial State:", state)

    for _ in range(10):
        action = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        state, reward, done = env.step(action)

        print("Action:", action)
        print("State:", state)
        print("Reward:", reward)
        print("Done:", done)

        if done:
            print("Finished!")
            break