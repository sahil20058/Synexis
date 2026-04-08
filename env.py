import random


class RescueEnv:
    def __init__(self, size=5):
        self.size = size
        self.max_steps = 20
        self.difficulty = "easy"
        self.reset()

    def reset(self):
        # Agent position
        self.agent_pos = [0, 0]

        # Random victim position (ensure it's not same as agent start)
        while True:
            self.victim_pos = [
                random.randint(0, self.size - 1),
                random.randint(0, self.size - 1)
            ]
            if self.victim_pos != self.agent_pos:
                break

        # State variables
        self.steps = 0
        self.total_reward = 0.0   # tracked for /score
        self.done = False

        return self.get_state()

    def get_state(self):
        return {
            "agent_pos": self.agent_pos,
            "victim_pos": self.victim_pos,
            "steps": self.steps,
            "max_steps": self.max_steps,
            "done": self.done
        }

    def step(self, action):
        if self.done:
            return self.get_state(), 0.0, True

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
            reward = 1.0
            self.done = True

        self.steps += 1
        self.total_reward += reward  # accumulate reward

        # End if max steps reached
        if self.steps >= self.max_steps:
            self.done = True

        return self.get_state(), reward, self.done